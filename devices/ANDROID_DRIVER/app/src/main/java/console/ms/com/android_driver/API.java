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
import java.util.Date;
import java.util.Set;

public class API {

    //private ServizioADTW servizioADTW;
    private SensorsOnBoard sensorsOnBoard;
    private ManageXml manageXml;
    private String html_index;
    private String html_404;




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




    private String Sensor(Uri uri){
        String result="";
        Set<String> args = uri.getQueryParameterNames();
        String limit = uri.getQueryParameter("limit");
        if(uri.getQueryParameter("type")!=null)
            result=sensorsOnBoard.getSensorActualValueByString(uri.getQueryParameter("type"));
        return result;
    }

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
                if (uri.getPath().equals("/sensor_act"))
                {
                    result = sensorsOnBoard.SensorActiveList().toString();
                    jsonObject.put("response",result);
                    jsonObject.put("timestamp", sdf.format(new Date()));
                    response = jsonObject.toString();
                    content = "application/json";
                }
                if (uri.getPath().equals("/sensor_active"))
                {
                    result = sensorsOnBoard.SensorActiveList().toString();
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
}




