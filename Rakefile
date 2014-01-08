task :default => [:spec] do
  # no default task, currently
end

task :spec do
  files = Dir["tests/*.spec"].join(" ")
  sh "rspec #{files}"
end

task :pretty_spec do
  files = Dir["tests/*.spec"].join(" ")
  sh "rspec --format documentation #{files}"
end

task :clean do
#  files = `find . -name '*~' -print`.
# how to get multi-line find output into a quoted form for rm
  files = Dir["*~", "*/*~", "*/*/*~"].join(" ")
  sh "rm #{files}"
end

task :this, [:target] do | task, args|
  sh "rspec tests/#{args[:target]}.spec"
end
