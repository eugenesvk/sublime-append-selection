import sublime
from sublime import RegionFlags
import sublime_plugin
import re

re_sp = re.compile(r'\s+')

import logging
DEFAULT_LOG_LEVEL = logging.WARNING
_log = logging.getLogger(__name__) # AppendSelection.append_seletion
_log.setLevel(DEFAULT_LOG_LEVEL)

plugin_cfg_file = 'AppendSelection.sublime-settings'
plugin_reg_nm   = 'append_selection'

def plugin_loaded():
  global Cfg, subl_set

  subl_set = sublime.load_settings(plugin_cfg_file)
  Cfg.load();

  subl_set.clear_on_change('AppendSelection')
  subl_set.add_on_change  ('AppendSelection', lambda: Cfg.load())


subl_region_flag ={ # https://www.sublimetext.com/docs/api_reference.html#sublime.RegionFlags 4132 3.8
  'NONE'                   	: RegionFlags.NONE                   	, #
  'DRAW_EMPTY'             	: RegionFlags.DRAW_EMPTY             	, # Draw empty regions with a vertical bar. By default, they aren’t drawn at all.
  'HIDE_ON_MINIMAP'        	: RegionFlags.HIDE_ON_MINIMAP        	, # Don’t show the regions on the minimap.
  'DRAW_EMPTY_AS_OVERWRITE'	: RegionFlags.DRAW_EMPTY_AS_OVERWRITE	, # Draw empty regions with a horizontal bar instead of a vertical one.
  'PERSISTENT'             	: RegionFlags.PERSISTENT             	, # Save the regions in the session.
  'DRAW_NO_FILL'           	: RegionFlags.DRAW_NO_FILL           	, # Disable filling the regions, leaving only the outline.
  'HIDDEN'                 	: RegionFlags.HIDDEN                 	, # Don’t draw the regions.
  'DRAW_NO_OUTLINE'        	: RegionFlags.DRAW_NO_OUTLINE        	, # Disable drawing the outline of the regions.
  'DRAW_SOLID_UNDERLINE'   	: RegionFlags.DRAW_SOLID_UNDERLINE   	, # Draw a solid underline below the regions.
  'DRAW_STIPPLED_UNDERLINE'	: RegionFlags.DRAW_STIPPLED_UNDERLINE	, # Draw a stippled underline below the regions.
  'DRAW_SQUIGGLY_UNDERLINE'	: RegionFlags.DRAW_SQUIGGLY_UNDERLINE	, # Draw a squiggly underline below the regions.
  'NO_UNDO'                	: RegionFlags.NO_UNDO                	, #
}

class Cfg():

  @staticmethod
  def load():
    reg_flags_def	= RegionFlags.DRAW_EMPTY and RegionFlags.DRAW_NO_FILL  # outline only
    if (reg_flags := subl_set.get('reg_flags')):
      if not isinstance(reg_flags, list):
        _log.error(f'‘reg_flags’ setting@‘{plugin_cfg_file}’ should be a ‘list’, not {type(reg_flags)} , ignoring and using defaults')
        Cfg.reg_flags	= reg_flags_def
      else:
        reg_flags_parsed = RegionFlags.NONE
        for flag in reg_flags:
          reg_flags_parsed |= subl_region_flag.get(flag.upper(),RegionFlags.NONE)
        Cfg.reg_flags	= reg_flags_parsed
        _log.debug(f'parsed ‘reg_flags’ from setting@‘{plugin_cfg_file}’ as {reg_flags_parsed}')


selection_added = False

import functools

def alias(aliases:dict):
  """
  function decorator that allows adding custom aliases to function arguments
  @alias({'offset':['o','off']}) # use a list of aliases or a single str alias ‘...:'o'’
  def demo(offset='default_offset', **kwargs):
    print(offset)
  demo(offset="arg_is_offset")	# arg_is_offset
  demo(o="arg_is_o")          	# arg_is_o
  demo(off="arg_is_off")      	# arg_is_off
  demo(noals="arg_is_noals")  	# default_offset !! NO alias for ‘noals’
  demo()                      	# default_offset
  """
  def decorator(func): # func.__name__=run
    @functools.wraps(func)
    def wrapper(self,*args,**kwargs):
      for name, alias in aliases.items():
        if not type(alias) is list:
          alias = [alias]
        for als in alias:
          if   name not in kwargs\
           and als      in kwargs:
            kwargs[name] = kwargs[als] # store the value of the aliased arg to our main arg
      return func(self,*args,**kwargs)
    return wrapper
  return decorator

from typing import List
class AppendSeletion(sublime_plugin.TextCommand):
  def __init__(self, view):
    super().__init__(view)
    self.last_word = None
    self.last_wordb = None

  @alias({'word':['w','ω'],'wordb':['wb','ωb'],'backward':['←'],'skip':['↷'],'wrap':['🗘'],'repeat_last_with_skip':['🔁','🔁↷','↷🔁']})
  def run(self, edit, word:bool=True, wordb:bool=True, backward = False, skip = False, wrap = False,
    repeat_last_with_skip = False, show:List[str]=["surround","animate"], **kwargs):

    if repeat_last_with_skip:
      word = self.last_word
      wordb = self.last_wordb
      backward = self.last_backward
      skip = True

    self.last_word = word
    self.last_wordb = wordb
    self.last_backward = backward

    sels = self.view.sel()
    if len(sels) == 0:
      return

    result = self._get_next_selection(sels, word, wordb, backward)

    if result == None:
      return

    sel, matches, shift = result
    self._append_selection(skip, sel, backward, matches, shift, show)

    global selection_added
    selection_added = True

  def _append_selection(self, skip, sel, backward, matches, shift, show):
    try:
      match = matches.__next__()
    except StopIteration:
      return

    start, end = match.start(1) + shift, match.end(1) + shift
    if sel.a > sel.b:
      start, end = end, start

    selection = sublime.Region(start, end)
    if skip:
      self.remove_xst_selection(backward)

    self.view.sel().add(selection)
    show_args = []
    if show: # Move viewport to show the new selection
      if   isinstance(show,list):
        show_args = [s.lower() if isinstance(s,str) else None for s in show]
      elif isinstance(show,str):
        show_args = re.split(re_sp,show.lower())
      #             	                       	                  ≝
      show_surrounds	= False if 'nosurround'	in show_args else True 	# show the surrounding context around the location
      keep_to_left  	= True  if 'left'      	in show_args else False	# keep the view to the left if horizontal scrolling is possible (4075)
      animate       	= False if 'noanimate' 	in show_args else True 	# animate scrolling (4075)
      self.view.show(location=selection, show_surrounds=show_surrounds, keep_to_left=keep_to_left, animate=animate)
      # location	scroll the view to this, for a Selection only the first Region is shown

    regions = []
    for match in matches:
      start, end = match.start(1) + shift, match.end(1) + shift
      regions.append(sublime.Region(start, end))

    self.view.erase_regions(plugin_reg_nm)
    regFlags = Cfg.reg_flags
    self.view.add_regions  (plugin_reg_nm, regions, 'string', '', regFlags)

  def remove_xst_selection(self,backward):
    forward = not backward
    sels = self.view.sel()

    old = []
    for index, sel in enumerate(sels):
      if (forward  and index == len(sels) - 1)\
      or (backward and index == 0            ):
        continue
      old.append(sel)

    self  .view.sel().clear()
    for sel in old:
      self.view.sel().add(sel)

  def _get_next_selection(self, sels, word, wordb, backward):
    if backward:
      sel = sels[ 0]
    else:
      sel = sels[-1]

    if sel.empty():
      sel = self.view.word(sel.b)
      if sel.empty():
        return None
      cursor = sel.end  () if backward else sel.begin()
    else:
      cursor = sel.begin() if backward else sel.end  ()

    selected = self.view.substr(sel)
    if backward:
      region = sublime.Region(0, cursor)
    else:
      region = sublime.Region(cursor, self.view.size())

    text = self.view.substr(region)

    re_w = (r'\b' if wordb else r'\W') if word else r'' # \b = word boundary, selects cur word
    matches = re.finditer(fr'{re_w}({re.escape(selected)}){re_w}', text)

    if backward:
      matches = reversed(list(matches))

    return sel, matches, region.a

class AppendSeletionListener(sublime_plugin.EventListener):
  def on_selection_modified_async(self, view):
    global selection_added
    if selection_added:
      selection_added = False
      return

    view.erase_regions(plugin_reg_nm)
