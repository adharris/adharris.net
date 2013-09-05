# _plugins/my-plugin.rb
require "jekyll-sass"

# module Jekyll

#   class MyGenerator < Generator
#     priority :lowest

#     def initialize(config)
#       config['map'] = {}
#       models = config['jekyll_models']
#       models.each do |model_type|
#         config['map'][model_type] = {}
#         config[model_type].each do |model|
#           config['map'][model_type][model['mdl_name']] = model
#         end
#       end
#     end

#     def generate(site)
#     end
#   end
# end
