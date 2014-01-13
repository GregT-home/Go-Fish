require 'sass/plugin/rack'
require './GoFish_app'

# nested - shows structure
# expanded - most human readable
# compact - one line per directive
# compressed - most efficient for the machine
Sass::Plugin.options[:style] = :nested
use Sass::Plugin::Rack

run GoFishApp

