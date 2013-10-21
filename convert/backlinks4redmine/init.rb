#svilend 2010-2013
#the directory should live in $redmine/lib/plugins/

Redmine::WikiFormatting::Macros.register do
    #     desc "This is my macro"
    #     macro :my_macro do |obj, args|
    #       "My macro output"
    #     end
    #
    #     desc "This is my macro that accepts a block of text"
    #     macro :my_macro do |obj, args, text|
    #       "My macro output"
    #     end
    #   end

#XXXXXXXXXXXX svd: part from child_pages, part from SearchController.index, part from render_page_hierarchy

  desc "shows backlinks to the/a wiki page. Example:\n\n  !{{backlinks}} or !{{backlinks(Foo)}} "
  macro :backlinks do |obj, args|
    title = nil
    if args.size > 0
      page = Wiki.find_page(args.first.to_s, :project => @project)
    elsif obj.is_a?(WikiContent) || obj.is_a?(WikiContent::Version)
      page = obj.page
      title = 'here'
    else
      raise 'With no argument, this macro can be called from wiki pages only.'
    end
    raise 'Page not found' if page.nil? || !User.current.allowed_to?(:view_wiki_pages, page.wiki.project)

    r,c = WikiPage.search( "[["+page.title, @project ,
      :all_words => true ,
      :titles_only => false
      #,:limit => 100,
      #,:offset => 0
      )
    title = page.pretty_title if title.nil?
    content = ''
      content << "links to " + title + ": "
      #content << "<ul> "

      r.each do |p|
        #content << "<li>"
        content << link_to( h(p.pretty_title),
                            { 	:controller => 'wiki', :action => 'show',
                                :project_id => p.project, :id => p.title },
                           :title => nil)
        content << "\n"
        #content << "</li>\n"
      end
      #content << "</ul>\n"
    content.html_safe
  end
end

# vim:ts=4:sw=4:expandtab
