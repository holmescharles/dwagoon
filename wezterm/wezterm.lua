local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.audible_bell = "Disabled"

config.hide_tab_bar_if_only_one_tab = true

-- Color scheme (wal)
local wal_cache = wezterm.home_dir .. "/.cache/wal"
config.color_scheme_dirs = { wal_cache }
config.color_scheme = 'wezterm-wal'
wezterm.add_to_config_reload_watch_list(wal_cache .. "/wezterm-wal.toml")

-- Window appearance
config.window_background_opacity = 0.9
config.macos_window_background_blur = 50
config.window_padding = {
  left = "2cell",
  right = "2cell",
  top = "1cell",
  bottom = "1cell"
}

return config
