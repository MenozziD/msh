package console.ms.com.android_driver;

import android.hardware.Sensor;
import android.net.Uri;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.Set;

public class API {

    //private ServizioADTW servizioADTW;
    private SensorsOnBoard sensorsOnBoard;
    private ManageXml manageXml;
    private String html_index;
    private String html_404;
    static String [] arraySettings= {"devicename","autoupdate","timeupdate"};


    public API(SensorsOnBoard sensorsOnBoard,String html_index,String html_404,ManageXml manageXml){
        //this.servizioADTW = servizioADTW;
        String html_file=FileManager.ReadFile(FileManager.path+FileManager.getFileSeparator()+ FileManager.main_dir_name+FileManager.getFileSeparator()+ FileManager.webui_dir_name+FileManager.getFileSeparator(),FileManager.webui_file_name);
        this.sensorsOnBoard=sensorsOnBoard;
        if (html_file!=null)
            this.html_index=html_file;
        else
            this.html_index=html_index;

        this.manageXml=manageXml;
        this.html_404=html_404;

    }


    public String Settings(Uri uri){
        String result=null;
        manageXml.readXml();
        JSONObject jsonObject=null;
        try {
            jsonObject = new JSONObject();
            if(uri.getQueryParameter("cmd")!=null && uri.getQueryParameter("setting")!=null) {
                if (uri.getQueryParameter("setting").equals("autoupdate")) {
                    if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                    {
                        manageXml.set_autoupdate(uri.getQueryParameter("value"));
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_autoupdate());
                    }
                    if (uri.getQueryParameter("cmd").equals("get"))
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_autoupdate());
                }
                if (uri.getQueryParameter("setting").equals("timeupdate")) {
                    if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                    {
                        manageXml.set_timeupdate(uri.getQueryParameter("value"));
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_timeupdate());
                    }
                    if (uri.getQueryParameter("cmd").equals("get"))
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_timeupdate());
                }
                if (uri.getQueryParameter("setting").equals("devicename")) {
                    if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                    {
                        manageXml.set_devicename(uri.getQueryParameter("value"));
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_devicename());
                    }
                    if (uri.getQueryParameter("cmd").equals("get"))
                        jsonObject.put(uri.getQueryParameter("setting"),manageXml.get_devicename());

                }
                if (result.equals(""))
                    jsonObject.put(uri.getQueryParameter("setting"),"Invalid setting");
            }
            if(uri.getQueryParameter("list")!=null ) {
                if(uri.getQueryParameter("list").equals("all") )
                {
                    jsonObject.put("number",arraySettings.length);
                    jsonObject.put("settings", Arrays.toString(arraySettings));
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        } finally
        {
            result=jsonObject.toString();
            return result;
        }
    }

    public String Sensor(Uri uri){
        String result=null;
        if(uri.getQueryParameter("type")!=null) {
            if (sensorsOnBoard.getSensorByString(uri.getQueryParameter("type"))!=null)
                result = sensorsOnBoard.SensorToJSON(sensorsOnBoard.getSensorByString(uri.getQueryParameter("type"))).toString();
            else
                result="NOT INSTALL";
        }
        if(uri.getQueryParameter("list")!=null)
            result = sensorsOnBoard.SensorList(uri.getQueryParameter("list")).toString();
        return result;
    }
/*
    public String route(String request) {
        String result = "";
        String content = "";
        String response = "";
        JSONObject jsonObject;
        Uri uri = Uri.parse(request);
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

        try {
            jsonObject = new JSONObject();

            jsonObject.put("request", uri.toString());
            jsonObject.put("response", "");
            jsonObject.put("timestamp", "");

            if(uri.getPath()!=null) {
                if (uri.getPath().equals("/sensor"))
                {
                    if(uri.getQueryParameter("type")!=null) {
                        if (sensorsOnBoard.getSensorByString(uri.getQueryParameter("type"))!=null)
                            result = sensorsOnBoard.SensorToJSON(sensorsOnBoard.getSensorByString(uri.getQueryParameter("type"))).toString();
                        else
                            result="NOT INSTALL";
                    }
                    if(uri.getQueryParameter("list")!=null)
                        result = sensorsOnBoard.SensorList(uri.getQueryParameter("list")).toString();
                    jsonObject.put("response",result);
                    jsonObject.put("timestamp", sdf.format(new Date()));
                    response = jsonObject.toString();
                    content = "application/json";

                }
                if (uri.getPath().equals("/settings"))
                {
                    if(uri.getQueryParameter("cmd")!=null && uri.getQueryParameter("setting")!=null) {
                        if (uri.getQueryParameter("setting").equals("autoupdate")) {
                            if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                                manageXml.set_autoupdate(uri.getQueryParameter("value"));
                            if (uri.getQueryParameter("cmd").equals("get"))
                                result = manageXml.get_autoupdate();
                        }
                        if (uri.getQueryParameter("setting").equals("timeupdate")) {
                            if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                                manageXml.set_timeupdate(uri.getQueryParameter("value"));
                            if (uri.getQueryParameter("cmd").equals("get"))
                                result = manageXml.get_timeupdate();
                        }
                        if (uri.getQueryParameter("setting").equals("h1")) {
                            if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null)
                                manageXml.set_h1(uri.getQueryParameter("value"));
                            if (uri.getQueryParameter("cmd").equals("get"))
                                result = manageXml.get_h1();

                        }
                    }
                    if(uri.getQueryParameter("setting_list")!=null)
                    {
                        String [] settings=new String[3];
                        settings[0]="autoupdate";
                        settings[1]="timeupdate";
                        settings[2]="h1";
                        result=settings.toString();
                    }

                    if (result.equals(""))
                        result=result="Invalid request\n"+uri.getQueryParameter("setting");

                    if (result.equals(""))
                        result=uri.getQueryParameter("setting")+" impostato a "+uri.getQueryParameter("value");

                    jsonObject.put("response",result);
                    jsonObject.put("timestamp", sdf.format(new Date()));
                    response = jsonObject.toString();
                    content = "application/json";
                }
                if (content.equals(""))
                {
                    if (uri.getPath().equals("/")) {
                        response = html_index;
                        response += "\r\n";
                        content = "text/html";
                    }else{
                        response = html_404;
                        response += "\r\n";
                        content = "text/html";
                    }
                }
            }
        } catch (JSONException e) {
            response = e.toString();
            e.printStackTrace();
            FileManager.Log(e.toString(), FileManager.Log_Error);
        } catch (Exception e) {
            response = e.toString();
            e.printStackTrace();
            FileManager.Log(e.toString(), FileManager.Log_Error);
        } finally {

            result = "HTTP/1.0 200" + "\r\n";
            result += "Content type: " + content + "\r\n";
            result += "Content length: " + response.length() + "\r\n";
            result += "\r\n";
            result += response;

            return result;
        }

    }
*/
}




