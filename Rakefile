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
  files = Dir["*~", "tests/*~"].join(" ")
  sh "rm -f #{files}"
end

task :game do
  rspec game.spec
end

task :card do
  rspec card.spec
end

task :deck do
  rspec deck.spec
end

task :hand do
  rspec hand.spec
end

