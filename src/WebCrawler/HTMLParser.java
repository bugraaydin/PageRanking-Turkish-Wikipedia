package WebCrawler;

        import org.json.JSONArray;
        import org.json.JSONObject;
        import org.jsoup.Jsoup;
        import org.jsoup.nodes.Document;
        import org.jsoup.nodes.Element;
        import org.jsoup.select.Elements;

        import java.io.*;
        import java.util.ArrayDeque;
        import java.util.Queue;


public class HTMLParser{
    static Queue<String> pagesToProcess = new ArrayDeque<String>();
    static int threadCount = 1;
    static final int MAX_THREAD = 5;
    public static final String path = "data/pages/";
    public static final String wikipediaDefault = "https://tr.wikipedia.org/wiki/";
    public static void main(String[] args) throws Exception{
        pagesToProcess.add("Ajdar");
        String pageToProcess = "";
        while(pagesToProcess.peek() != null) {
            parsePage(pagesToProcess.poll());
        }

    }
    public static void parsePage(String pageName){
        JSONObject json = new JSONObject();
        JSONArray pageNames = new JSONArray();
        JSONArray pageUrls = new JSONArray();
        String url = wikipediaDefault + pageName;
        System.out.println("Fetching %s..." + url);
        try {
            Document doc = Jsoup.connect(url).get();
            Elements links = doc.select("div#bodyContent");
            links = doc.select("a[href^=/wiki]");
            for (Element link : links) {
                if(link.text() != "") {
                    pageNames.put(link.text());
                    pagesToProcess.add(link.text());
                    //pageUrls.put(link.attr("href"));
                    pageUrls.put(java.net.URLDecoder.decode(link.attr("href"), "UTF-8"));
                }
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
        catch(Exception e){
            System.err.println("Failed crawling page: " + url );
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