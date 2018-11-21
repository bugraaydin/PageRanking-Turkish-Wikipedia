package WebCrawler;

public class Page {
    private String url;
    private String pageName;

    public Page(String url, String pageName){
        this.url = url;
        this.pageName = pageName;
    }

    public String getPageName(){
        return pageName;
    }
    public String getUrl(){
        return url;
    }
    public String toString(){
        return pageName + "," + url + "\n";
    }
}
