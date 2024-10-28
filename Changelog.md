# Changelog
All notable changes to this project will be documented in this file

[unreleased]: https://github.com/shagabutdinov/sublime-append-selection/compare/st4-0.5.0...HEAD
## [Unreleased]
<!-- - __Added__ -->
  <!-- + :sparkles:  -->
  <!-- new features -->
<!-- - __Changed__ -->
  <!-- +   -->
  <!-- changes in existing functionality -->
<!-- - __Fixed__ -->
  <!-- + :beetle:  -->
  <!-- bug fixes -->
<!-- - __Deprecated__ -->
  <!-- + :poop:  -->
  <!-- soon-to-be removed features -->
<!-- - __Removed__ -->
  <!-- + :wastebasket:  -->
  <!-- now removed features -->
<!-- - __Security__ -->
  <!-- + :lock:  -->
  <!-- vulnerabilities -->

[st4-0.5.0]: https://github.com/shagabutdinov/sublime-append-selection/releases/tag/st4-0.5.0
## [st4-0.5.0]
- __Added__
  + ✨ jump to the latest selected word instead of silently going offscreen (with extra options to show surrounding context/animate/keep left)
  + ✨ shorter argument aliases like `w` instead of `word`
  + ✨ option to use `\b` for word boundaries matching the default Sublime Text behavior (also selects current word)
  + ✨ user configuration of highlight style to match default outline and make it configurable
- __Changed__
  +  highlight style to outline only
- __Fixed__
  + 🐞 skipping while going in reverse direction moves selection [src](https://github.com/shagabutdinov/sublime-append-selection/issues/1)
