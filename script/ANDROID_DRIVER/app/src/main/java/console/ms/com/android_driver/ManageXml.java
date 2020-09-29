package console.ms.com.android_driver;

import android.util.Xml;

import org.json.JSONObject;
import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;
import org.xmlpull.v1.XmlSerializer;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;

public class ManageXml {

    private InputStream ist;
    private FileOutputStream ost;
    private XmlPullParser xrp;

    private boolean my_config;
    public void setMy_config(boolean value){my_config=value;}
    public boolean getMy_config(){return my_config;}

    private String devicename;
    private String autoupdate;
    private String timeupdate;




    // frontend_info
    public String getFrontEndInfo(String tag){
        String result=null;
        switch(tag) {
            case "devicename":
                result=devicename;
                break;
            case "autoupdate":
                result=autoupdate;
                break;
            case "timeupdate":
                result=timeupdate;
                break;
        }
        return result;
    }

    public void setFrontEndInfo(String tag,String val){
        switch(tag) {
            case "devicename":
                devicename=val;
                break;
            case "autoupdate":
                autoupdate=val;
                break;
            case "timeupdate":
                timeupdate=val;
                break;
        }
    }

    public ManageXml(){
        my_config=false;
        devicename ="ADTW";
        timeupdate="5000";
        autoupdate="false";
    }

    public void writeXml() {
        XmlSerializer xmlSerializer = Xml.newSerializer();
        StringWriter writer = new StringWriter();
        try {
            xmlSerializer.setOutput(writer);
            xmlSerializer.startDocument("UTF-8", true);

            xmlSerializer.startTag("", "settings");

            xmlSerializer.startTag("", "frontend_info");

            xmlSerializer.startTag("", "devicename");
            xmlSerializer.attribute("","value", devicename);
            xmlSerializer.endTag("", "devicename");

            xmlSerializer.startTag("", "autoupdate");
            xmlSerializer.attribute("","value", autoupdate);
            xmlSerializer.endTag("", "autoupdate");

            xmlSerializer.startTag("", "timeupdate");
            xmlSerializer.attribute("","value", timeupdate);
            xmlSerializer.endTag("", "timeupdate");

            xmlSerializer.endTag("", "frontend_info");

            xmlSerializer.endTag("", "settings");

            xmlSerializer.endDocument();

            ost.write(writer.toString().getBytes());
            ost.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public void readXml(){
        boolean frontend_info = false;
        boolean app_info = false;

        try {
            if (my_config){
                xrp = Xml.newPullParser();
                xrp.setInput(ist, null);
            }
            int event = xrp.getEventType();
            while (event != XmlPullParser.END_DOCUMENT)  {
                String name=xrp.getName();
                switch (event){
                    case XmlPullParser.START_TAG:
                        if(name.equals("frontend_info"))
                            frontend_info = true;
                        if(name.equals("app_info"))
                            app_info = true;
                        if (name.equals("devicename")&& frontend_info)
                            devicename =xrp.getAttributeValue(0);
                        if (name.equals("autoupdate")&& frontend_info)
                            autoupdate=xrp.getAttributeValue(0);
                        if (name.equals("timeupdate")&& frontend_info)
                            timeupdate=xrp.getAttributeValue(0);
                        break;
                }
                event = xrp.next();
            }
        } catch (XmlPullParserException | IOException e) {
            e.printStackTrace();
        }
    }

    public void setXrp(XmlPullParser xrp) {
        this.xrp = xrp;
    }

    public void setIst(InputStream ist) {
        this.ist = ist;
    }

    public void setOst(FileOutputStream ost) {
        this.ost = ost;
    }

}
