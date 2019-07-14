package console.ms.com.android_driver;


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

import android.hardware.Sensor;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.support.v7.app.AppCompatActivity;
import android.widget.EditText;
import android.widget.TextView;
import android.os.Bundle;


public class MainActivity extends AppCompatActivity  {

    EditText welcomeMsg;
    TextView infoIp;
    private TextView[] tvSensori;
    TextView infoMsg;
    String msgLog = "";
    String res_text="";
    String temp_text="0.0°C";
    ServerSocket httpServerSocket;

    private SensorManager sensorManager;
    private SensorsOnBoard sensorsOnBoard;

    @Override
    protected void onResume() {
        super.onResume();
        for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
        {
            sensorManager.registerListener(sensorsOnBoard.getListenerSensore(i), sensorsOnBoard.getSensore(i), SensorManager.SENSOR_DELAY_FASTEST);
            //sensorManager.registerListener(lightEventListener, lightSensor, SensorManager.SENSOR_DELAY_FASTEST);
        }

    }

    @Override
    protected void onPause() {
        super.onPause();
        for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
        {
            sensorManager.unregisterListener(sensorsOnBoard.getListenerSensore(i));
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        welcomeMsg = (EditText) findViewById(R.id.welcomemsg);
        //welcomeMsg.setText(this.getResources().getText(R.string.index_html));
        res_text=this.getResources().getText(R.string.index_html).toString();
        infoIp = (TextView) findViewById(R.id.infoip);
        infoMsg = (TextView) findViewById(R.id.msg);
        tvSensori= new TextView[3];
        tvSensori[0] = (TextView) findViewById(R.id.tvTYPE_MAGNETIC_FIELD);
        tvSensori[1] = (TextView) findViewById(R.id.tvTYPE_LIGHT);
        tvSensori[2] = (TextView) findViewById(R.id.tvTYPE_PROXIMITY);
        String s=getIpAddress() + ":" + HttpServerThread.HttpServerPORT + "\n";
        System.out.print(s);
        infoIp.setText(getIpAddress() + ":" + HttpServerThread.HttpServerPORT + "\n");

        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        sensorsOnBoard= new SensorsOnBoard(sensorManager,tvSensori);
        infoMsg.append("\n"+sensorsOnBoard.scanSensors());

        HttpServerThread httpServerThread = new HttpServerThread();
        httpServerThread.start();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if (httpServerSocket != null) {
            try {
                httpServerSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private String getIpAddress() {
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
                        ip += "SiteLocalAddress: "
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

    private class HttpServerThread extends Thread {

        static final int HttpServerPORT = 8888;
        SensorManager mSensorManager;
        Sensor mTempSensor;

        @Override
        public void run() {
            Socket socket = null;

            try {
                httpServerSocket = new ServerSocket(HttpServerPORT);
                res_text.replace("%TEMP", temp_text);

                while(true){
                    socket = httpServerSocket.accept();
                    HttpResponseThread httpResponseThread =
                            new HttpResponseThread(
                                    socket,
                                    res_text);
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
        String h1;

        HttpResponseThread(Socket socket, String msg){
            this.socket = socket;
            h1 = msg;
        }

        @Override
        public void run() {
            BufferedReader is;
            PrintWriter os;
            String request;
            String arequest[];


            try {
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                request = is.readLine();

                os = new PrintWriter(socket.getOutputStream(), true);


                arequest=request.split(" ");
                msgLog +="Method:".concat(arequest[0]+"\n");
                msgLog +="Resource:".concat(arequest[1]+"\n");
                msgLog +="HTTP Version:".concat(arequest[2]+"\n");

                String response = h1;

                os.print("HTTP/1.0 200" + "\r\n");
                os.print("Content type: text/html" + "\r\n");
                os.print("Content length: " + response.length() + "\r\n");
                os.print("\r\n");
                os.print(response + "\r\n");
                os.flush();
                socket.close();


                //msgLog += "Request of " + request
                //+ " from " + socket.getInetAddress().toString() + "\n";
                //msgLog += "Request of " + request;
                MainActivity.this.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {

                        infoMsg.setText(msgLog);
                    }
                });

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            return;
        }
    }

}
