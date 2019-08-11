package console.ms.com.android_driver;

import android.hardware.Sensor;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;

public class API {

    private ServizioADTW servizioADTW;

    public API(ServizioADTW servizioADTW) {
        this.servizioADTW = servizioADTW;
    }

    public String route(String request) {
        String result = "";
        String content = "";
        String response = "";
        JSONObject jsonObject;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

        try {

            jsonObject = new JSONObject();
            jsonObject.put("request", request);
            jsonObject.put("response", "");
            jsonObject.put("timestamp", "");

            if (request.trim().equals("/")) {
                response = servizioADTW.getString(R.string.html_index);
                response += "\r\n";
                content = "text/html";
            }

            if (request.indexOf("/sensor") > -1) {
                String[] arr = request.split("\\?");
                arr = arr[1].split("=");
                if (arr[0].equals("type")) {
                    if (arr[1].equals("LIGHT"))
                        jsonObject.put("response", servizioADTW.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_LIGHT).getActualValue());
                    if (arr[1].equals("MAGNETIC_FIELD"))
                        jsonObject.put("response", servizioADTW.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_MAGNETIC_FIELD).getActualValue());
                    if (arr[1].equals("PROXIMITY"))
                        jsonObject.put("response", servizioADTW.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_PROXIMITY).getActualValue());
                }
                jsonObject.put("timestamp", sdf.format(new Date()));
                response = jsonObject.toString();
                content = "application/json";
            }

            if (request.indexOf("/settings") > -1) {
                String[] arr = request.split("\\?");
                arr = arr[1].split("=");
                if (arr[0].equals("str_set")) {
                    if (arr[1].equals("time_update"))
                        jsonObject.put("response", servizioADTW.getManageXml().get_timeupdate());
                    if (arr[1].equals("device_name"))
                        jsonObject.put("response", servizioADTW.getManageXml().get_h1());
                }
                jsonObject.put("timestamp", sdf.format(new Date()));
                response = jsonObject.toString();
                content = "application/json";
            }
            if (content.equals("")) {
                response = servizioADTW.getString(R.string.html_404);
                response += "\r\n";
                content = "text/html";
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



