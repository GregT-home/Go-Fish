task :default => [:spec] do
  # no default task, currently
end

desc "Run rspec over the entire project"
task :spec do
  files = Dir["specs/*.spec"].join(" ")
  sh "rspec #{files}"
end

desc "Run rspec tests in pretty (doc) format"
task :pretty_spec do
  files = Dir["specs/*.spec"].join(" ")
  sh "rspec --format documentation #{files}"
end

desc "Delete standard temporary files, Emacs *~ files, in particular"
task :clean do
  sh 'find . -name "*~" -exec rm -v {} \;'
  sh 'rm -f tmp-pagedump.html'
end

desc "Run rspec over :target"
task :this, [:target] do | task, args|
  sh "rspec specs/#{args[:target]}.spec"
end

desc "Run rspec tests on :target in pretty (doc) format"
task :this_pretty, [:target] do | task, args|
  sh "rspec --format documentation specs/#{args[:target]}.spec"
end

desc "Run spinach tests"
task :spinach do
  sh "spinach"
end

desc "Run spinach generate"
task :spinach_gen do
  sh "spinach --generate"
end

desc "Run spinach on :target"
task :spin, [:target] do | task, args |
  sh "spinach -t #{args[:target]}"
end
