package WebCrawler;

import org.json.*;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class HTMLParser{
    public static final String path = "data/pages/";
    public static final String wikipediaDefault = "https://tr.wikipedia.org/wiki/";
    public static void main(String[] args) throws Exception{
        String startingPage = "JavaScript";
        parsePage(startingPage);

    }
    public static void parsePage(String pageName) throws Exception{
        ArrayList<Page> pages = new ArrayList<Page>();
        JSONObject json = new JSONObject();
        String url = wikipediaDefault + pageName;
        System.out.println("Fetching %s..." + url);

        Document doc = Jsoup.connect(url).get();
        Elements links = doc.select("a[href^=/wiki]");
        for (Element link : links) {
            Page newPage = new Page(link.attr("href"), link.text());
            pages.add(newPage);
        }
        PrintWriter out = new PrintWriter(path+pageName+".txt");
        for (Page page : pages) {
            Thread newJob = new Thread() {
                public void run() {
                    try {
                        parsePage(page.getPageName());
                    } catch (
                            Exception e)
                    {
                        e.printStackTrace();
                    }
                }
            };
            newJob.start();
            out.println(page.getPageName() + "*" + page.getUrl());
        }
        out.flush();
        out.close();
    }


}
