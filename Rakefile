task :default => [:spec] do
  # no default task, currently
end

task :spec do
  files = Dir["specs/*.spec"].join(" ")
  sh "rspec #{files}"
end

task :pretty_spec do
  files = Dir["specs/*.spec"].join(" ")
  sh "rspec --format documentation #{files}"
end

task :clean do
#  files = Dir["*~", "*/*~", "*/*/*~"].join(" ")
#  sh "rm #{files}"
  sh 'find . -name "*~" -exec rm -v {} \;'
end

task :this, [:target] do | task, args|
  sh "rspec specs/#{args[:target]}.spec"
end
task :this_pretty, [:target] do | task, args|
  sh "rspec --format documentation specs/#{args[:target]}.spec"
end

task :spinach do
  sh "spinach"
end

task :spin, [:target] do | task, args |
  sh "spinach -t #{args[:target]}"
end
