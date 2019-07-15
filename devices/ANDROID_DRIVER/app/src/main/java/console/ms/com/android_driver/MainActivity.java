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
    TextView infoLog;
    private TextView[] tvSensori;
    TextView infoMsg;
    String res_text="";

    WebServer webServer;

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

    public String getSensorValue(Integer type)
    {
        return sensorsOnBoard.getSensoreValue(type);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        welcomeMsg = (EditText) findViewById(R.id.welcomemsg);
        //welcomeMsg.setText(this.getResources().getText(R.string.index_html));

        infoLog = (TextView) findViewById(R.id.infoip);
        infoMsg = (TextView) findViewById(R.id.msg);
        tvSensori= new TextView[3];
        tvSensori[0] = (TextView) findViewById(R.id.tvTYPE_MAGNETIC_FIELD);
        tvSensori[1] = (TextView) findViewById(R.id.tvTYPE_LIGHT);
        tvSensori[2] = (TextView) findViewById(R.id.tvTYPE_PROXIMITY);

        webServer=new WebServer(getString(R.string.index_html),this);
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        sensorsOnBoard= new SensorsOnBoard(sensorManager,tvSensori);
        webServer.getHttpServerThread().start();

        infoMsg.append(webServer.getIpAddress());
        infoMsg.append(":" + Integer.toString(webServer.HttpServerPORT )+ "\n");
        infoMsg.append("\n"+sensorsOnBoard.scanSensors());

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        webServer.close();

    }


}
