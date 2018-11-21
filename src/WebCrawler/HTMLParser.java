package WebCrawler;

import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class HTMLParser{
    static int threadCount = 1;
    static final int MAX_THREAD = 5;
    public static final String path = "data/pages/";
    public static final String wikipediaDefault = "https://tr.wikipedia.org/wiki/";
    public static void main(String[] args) throws Exception{
        String startingPage = "JavaScript";
        parsePage(startingPage);


    }
    public static void parsePage(String pageName) throws Exception{
        JSONObject json = new JSONObject();
        JSONArray pageNames = new JSONArray();
        JSONArray pageUrls = new JSONArray();
        String url = wikipediaDefault + pageName;
        System.out.println("Fetching %s..." + url);
        Document doc = Jsoup.connect(url).get();
        Elements links = doc.select("a[href^=/wiki]");
        for (Element link : links) {
            pageNames.put(link.text());
            pageUrls.put(link.attr("href"));
        }
        json.put("Names", pageNames);
        json.put("URLS", pageUrls);
        try(FileWriter file = new FileWriter("data/pages/" +pageName + ".json")){
            file.write(json.toString());
            file.flush();
            file.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
    synchronized static void incrementThreadCount(){
        threadCount++;
    }
    synchronized static void decrementThreadCount(){
        threadCount--;
    }
}

/*
            Thread newJob = new Thread() {
                public void run() {
                    try {
                        parsePage(link.text());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            };
                newJob.start();
                incrementThreadCount();
 */
