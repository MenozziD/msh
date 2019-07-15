package console.ms.com.android_driver;

import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.Enumeration;

public class WebServer {

    private String htmlHomepage;
    private HttpServerThread webHttpServerThread;
    //private HttpResponseThread webHttpResponseThread;
    MainActivity activity;
    ServerSocket httpServerSocket;
    static final int HttpServerPORT = 8888;
    static String msgLog="";

    public WebServer (String phtmlHomepage, MainActivity plogMainActivity)
    {
        activity=plogMainActivity;
        webHttpServerThread = new HttpServerThread();
        htmlHomepage=phtmlHomepage;
    }

    public HttpServerThread getHttpServerThread ()  { return webHttpServerThread; }


    public void close() {
        if (httpServerSocket != null) {
            try {
                httpServerSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public String getIpAddress() {
        String ip = "";
        try {
            Enumeration<NetworkInterface> enumNetworkInterfaces = NetworkInterface
                    .getNetworkInterfaces();
            while (enumNetworkInterfaces.hasMoreElements()) {
                NetworkInterface networkInterface = enumNetworkInterfaces
                        .nextElement();
                Enumeration<InetAddress> enumInetAddress = networkInterface
                        .getInetAddresses();
                while (enumInetAddress.hasMoreElements()) {
                    InetAddress inetAddress = enumInetAddress.nextElement();

                    if (inetAddress.isSiteLocalAddress()) {
                        ip += "IP Server : "
                                + inetAddress.getHostAddress() ; //+ "\n"
                    }
                }

            }

        } catch (SocketException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            ip += "Something Wrong! " + e.toString() + "\n";
        }

        return ip;
    }



    public class HttpServerThread extends Thread {

        public HttpServerThread()
        {}

        @Override
        public void run() {
            Socket socket = null;

            try {
                httpServerSocket = new ServerSocket(HttpServerPORT);

                while(true){
                    socket = httpServerSocket.accept();
                    HttpResponseThread httpResponseThread =
                            new HttpResponseThread(
                                    socket,
                                    htmlHomepage);
                    httpResponseThread.start();
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    private class HttpResponseThread extends Thread {

        Socket socket;
        String response;

        HttpResponseThread(Socket socket, String msg){
            this.socket = socket;
            response = msg;
        }

        @Override
        public void run() {
            BufferedReader is;
            PrintWriter os;
            String request;
            String arequest[];
            JSONObject jsonObject;

            try {
                jsonObject= new JSONObject();
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                request = is.readLine();

                os = new PrintWriter(socket.getOutputStream(), true);

                arequest=request.split(" ");
                msgLog +="Method:".concat(arequest[0]+"\n");
                msgLog +="Resource:".concat(arequest[1]+"\n");
                msgLog +="HTTP Version:".concat(arequest[2]+"\n");


                if (arequest[1].trim().equals("/actual_lx"))
                    jsonObject.put("response",activity.getSensorValue(Sensor.TYPE_LIGHT));
                else
                    jsonObject.put("response","NULL");

                response=jsonObject.toString();
                os.print("HTTP/1.0 200" + "\r\n");
                os.print("Content type: text/html" + "\r\n");
                os.print("Content length: " + response.length() + "\r\n");
                os.print("\r\n");
                os.print(response + "\r\n");
                os.flush();
                socket.close();

                activity.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        activity.infoLog.append(msgLog);
                    }
                });

                //msgLog += "Request of " + request
                //+ " from " + socket.getInetAddress().toString() + "\n";
                //msgLog += "Request of " + request;
                /*
                MainActivity.this.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {

                        infoMsg.setText(msgLog);
                    }
                });
                */


            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            catch (JSONException e) {
            e.printStackTrace();}

            return;
        }
    }


}
