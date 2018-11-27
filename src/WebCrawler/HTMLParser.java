package WebCrawler;

        import org.json.JSONArray;
        import org.json.JSONObject;
        import org.jsoup.Jsoup;
        import org.jsoup.nodes.Document;
        import org.jsoup.nodes.Element;
        import org.jsoup.select.Elements;

        import java.io.*;
        import java.util.*;


public class HTMLParser{
    static Set<String> uselessStrings = new HashSet<String>();
    static Set<String> alreadyParsedPages = new HashSet<String>();
    static Queue<String> pagesToProcess = new ArrayDeque<String>();

    public static Locale trlocale= new Locale("tr", "TR");
    public static final String wikipediaDefault = "https://tr.wikipedia.org/wiki/";
    public static void main(String[] args) throws Exception{
        ArrayList<String> useless = new ArrayList<String>();
        useless.add("mesaj"); useless.add(""); useless.add(" "); useless.add("sorumluluk reddi");
        useless.add("son değişiklikler"); useless.add("topluluk portali"); useless.add("yardım");
        useless.add("sayfaya bağlantılar"); useless.add("anasayfa"); useless.add("ilgili değişiklikler");
        useless.add("özel sayfalar"); useless.add("vikipedi hakkında"); useless.add("kaynak belirtilmeli");
        useless.add("kaynak gösterme şablonları"); useless.add("daha iyi kaynak gerekli"); useless.add("tartışma");
        useless.add("katkılar"); useless.add("oku"); useless.add("hakkımızda"); useless.add("içindekiler");
        useless.add("köy çeşmesi"); useless.add("iş birliği projesi"); useless.add("deneme tahtası"); useless.add("seçkin içerik"); useless.add("rastgele madde");
        useless.add("madde"); useless.add("ısbn sihirli bağlantısını kullanan sayfalar"); useless.add("kaynaksız anlatımlar içeren maddeler"); useless.add("bazı başlıkları geliştirilmeye ihtiyaç duyulan maddeler");
        updateUselessList(useless);
        queuePage("ajdar");

        dequeuePage();
        for(int i = 0; i < 500; i++) {
            Thread newJob = new Thread() {
                public void run() {
                    try {
                        while (!isEmpty()) {
                            dequeuePage();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            };
            newJob.start();
        }

    }
    static void updateUselessList(ArrayList<String> dictionary){
        for(String str : dictionary){
            uselessStrings.add(str);
        }
    }
    public static void parsePage(String pageName){
        String url = wikipediaDefault + pageName;
        System.out.println("Fetching %s..." + url);
        try {
            if(!alreadyParsedPages.add(pageName)){
                return;
            }
            if(uselessStrings.contains(pageName)){
                return;
            }
            Document doc = Jsoup.connect(url).get();
            JSONObject json = new JSONObject();
            JSONArray pageNames = new JSONArray();
            Elements links = doc.select("div#bodyContent");
            links = links.select("a[href^=/wiki]");
            for (Element link : links) {
                if(!(uselessStrings.contains(link.text().toLowerCase(trlocale))) && !link.text().contains("(anlam ayrımı)") && !link.text().equals("") && !link.attr("href").contains("svg")) {
                    pageNames.put(link.text().toLowerCase(trlocale));
                    pagesToProcess.add(link.text().toLowerCase(trlocale));
                    //pageUrls.put(link.attr("href"));
                }
            }
            json.put("Links", pageNames);
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
    synchronized static void queuePage(String str){
        pagesToProcess.add(str);
    }
    synchronized static void dequeuePage(){
        parsePage(pagesToProcess.poll());
    }
    synchronized static boolean isEmpty(){
        if(pagesToProcess.peek() != null)
            return false;
        return true;
    }
}