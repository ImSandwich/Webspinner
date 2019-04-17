/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlAnchor;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

import java.net.URLEncoder;
import java.util.HashMap;
import java.util.List;

public class WebScraper {

    static class WikipediaResponse
    {
        String pageName;
        HashMap<String, String> linkedPages;
        public WikipediaResponse(String name, HashMap<String, String> linked)
        {
            pageName = name;
            linkedPages = linked;
        }
    }

    public static WikipediaResponse scrapWikipedia(String searchQuery) {
        WebClient client = new WebClient();

        client.getOptions().setCssEnabled(false);
        client.getOptions().setJavaScriptEnabled(false);
        HashMap<String, String> linkedPages =  new HashMap<>();
        WikipediaResponse output = new WikipediaResponse(searchQuery, linkedPages);
        try
        {
            String searchUrl = "https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/" + URLEncoder.encode(searchQuery, "UTF-8") + "&limit=3";

            HtmlPage page = client.getPage(searchUrl);
            HtmlElement linksList = page.getHtmlElementById("mw-whatlinkshere-list");
            List<HtmlElement> listItems = linksList.getByXPath("./li");
            for (HtmlElement listItem : listItems)
            {
                HtmlAnchor anchor = listItem.getFirstByXPath("./a");
                if (anchor != null)
                {
                    String child = anchor.asText();
                    String url = anchor.getAttribute("href").split("/")[2];
                    linkedPages.put(child, url);
                }
            }


        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return output;
    }
}
