# Sublime AppendSelection plugin

Provides replacement for default sublime cursors appending.


### Demo

![Demo](https://github.com/shagabutdinov/sublime-enhanced-demos/raw/master/append_selection.gif "Demo")


### Reason

Sublime default "find_under_expand" worked pretty well but there was not enough
options for me. I added direction control (e.g. look backward/forward) and
search type (find part of word or whole word).


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

1. Select text forward
2. Select text backward
3. Select word forward
4. Select word forward


### Usage

Select a text or position cursor on top of word that should be selected several
times. Hit keyboard shortcuts to add next or previous occurence of word to
cursors. You can also skip last cursor and go to next selection.


### Commands

| Description          	|                	|                	|               	| Key          	| Command palette                       |
|----------------------	|----------------	|----------------	|---------------	|--------------	|---------------------------------------|
| Append next          	|                	|                	| <kbd>alt</kbd>	| <kbd>c</kbd> 	| AppendSelection: append next          |
| Append previous      	|<kbd>shift</kbd>	|                	| <kbd>alt</kbd>	| <kbd>c</kbd> 	| AppendSelection: append previous      |
| Append next word     	|                	|<kbd>ctrl</kbd> 	| <kbd>alt</kbd>	| <kbd>c</kbd> 	| AppendSelection: append next word     |
| Append previous word 	|<kbd>shift</kbd>	|<kbd>ctrl</kbd> 	| <kbd>alt</kbd>	| <kbd>c</kbd> 	| AppendSelection: append previous word |
| Skip cursor          	|<kbd>shift</kbd>	|<kbd>ctrl</kbd> 	|               	| <kbd>c</kbd> 	| AppendSelection: skip last            |


### Dependencies

None
