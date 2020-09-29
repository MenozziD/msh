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

import static android.content.Context.MODE_PRIVATE;

public class API {

    //private ServizioADTW servizioADTW;
    private SensorsOnBoard sensorsOnBoard;
    private ManageXml manageXml;
    private String html_index;
    private String html_404;
    static String [] arraySettings= {"devicename","autoupdate","timeupdate"};


    public API(SensorsOnBoard sensorsOnBoard,String html_index,String html_404,ManageXml manageXml){
        //this.servizioADTW = servizioADTW;
        String html_file=FileManager.ReadFile_Text(FileManager.path+FileManager.getFileSeparator()+ FileManager.main_dir_name+FileManager.getFileSeparator()+ FileManager.webui_dir_name+FileManager.getFileSeparator(),FileManager.webui_file_name).toString();
        this.sensorsOnBoard=sensorsOnBoard;
        if (html_file!=null)
            this.html_index=html_file;
        else
            this.html_index=html_index;

        this.manageXml=manageXml;
        this.html_404=html_404;

    }


    public String Settings(Uri uri){
        String[] listCmd={"get","set"};
        String result=null;
        manageXml.readXml();
        JSONObject jsonObject=null;
        try {
            jsonObject = new JSONObject();
            if(Arrays.asList(listCmd).contains(uri.getQueryParameter("cmd")) && uri.getQueryParameter("setting")!=null) {
                    if (uri.getQueryParameter("cmd").equals("set") && uri.getQueryParameter("value") != null) {
                        manageXml.setFrontEndInfo(uri.getQueryParameter("setting"), uri.getQueryParameter("value"));
                        manageXml.writeXml();
                    }
                    jsonObject.put(uri.getQueryParameter("setting"),manageXml.getFrontEndInfo(uri.getQueryParameter("setting")));
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

    public String Camera(Uri uri) {
        App app = App.getInstance();
        String result = null;
        if (uri.getQueryParameter("cmd").equals("start")) {
            //START REC
            if (!app.isServerServiceRunning(ServizioADTW.class))
                app.startCameraService();
                //STOP REC
            else
                app.stopCameraService();
        }
        return result;
    }

}




