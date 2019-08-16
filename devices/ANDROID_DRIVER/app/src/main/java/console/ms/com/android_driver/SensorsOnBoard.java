package console.ms.com.android_driver;

import android.annotation.TargetApi;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;

public class SensorsOnBoard  {

    static  Integer[] dizSensori;
    private Sensor[] sensori;
    private Integer[] sensoriKey;
    private String[] sensoriName;
    private AscoltatoreSensore[] sensoriListener;

    private SensorManager sensorManager;

    static final Integer maxNumberofSensor = 11;


    public SensorsOnBoard (SensorManager sensorManager)
    {
        this.sensorManager = sensorManager;
        sensoriKey= new Integer[maxNumberofSensor];
        sensori= new Sensor[maxNumberofSensor];
        sensoriListener = new AscoltatoreSensore[maxNumberofSensor];
        sensoriName= new String[maxNumberofSensor];
        for (int i =0; i < maxNumberofSensor ;i++)
        {
            if (i==0)  sensoriKey[i] = Sensor.TYPE_MAGNETIC_FIELD;
            if (i==1)  sensoriKey[i] = Sensor.TYPE_LIGHT;
            if (i==2)  sensoriKey[i] = Sensor.TYPE_PROXIMITY;
            if (i==3)  sensoriKey[i] = Sensor.TYPE_PRESSURE;
            if (i==4)  sensoriKey[i] = Sensor.TYPE_ACCELEROMETER;
            if (i==5)  sensoriKey[i] = Sensor.TYPE_AMBIENT_TEMPERATURE;
            if (i==6)  sensoriKey[i] = Sensor.TYPE_GYROSCOPE;
            if (i==7)  sensoriKey[i] = Sensor.TYPE_GRAVITY;
            if (i==8)  sensoriKey[i] = Sensor.TYPE_MOTION_DETECT;
            if (i==9)  sensoriKey[i] = Sensor.TYPE_RELATIVE_HUMIDITY;
            if (i==10)  sensoriKey[i] = Sensor.TYPE_STATIONARY_DETECT;
            sensoriName[i]=castIntToStrSensorType(sensoriKey[i]);
        }

        scanSensors();

        for (int i=0; i<maxNumberofSensor;i++) {
            if (sensori[i] != null)
                sensorManager.registerListener(sensoriListener[i], sensori[i], SensorManager.SENSOR_DELAY_FASTEST);
        }
    }


    public JSONObject SensorToJSON(Sensor s){
        JSONObject jsonObject=null;
        try{
            jsonObject = new JSONObject();
            jsonObject.put("name",s.getName());
            jsonObject.put("vendor",s.getVendor());
            jsonObject.put("version",Integer.toString(s.getVersion()));
            jsonObject.put("type",Integer.toString(s.getType()));
            jsonObject.put("maxRange",Float.toString(s.getMaximumRange()));
            jsonObject.put("resolution",Float.toString(s.getResolution()));
            jsonObject.put("power",Float.toString(s.getPower()));
            jsonObject.put("minDelay",Float.toString(s.getMinDelay()));
            jsonObject.put("actualValue",getSensorActualValueByKey(s.getType()));

        } catch (JSONException e) {
            e.printStackTrace();
        }finally
        {
            return jsonObject;
        }
    }


    public JSONObject SensorList(String param) {
        JSONObject jsonObject=null;
        jsonObject = new JSONObject();

        String[] sensorsNames= new String[maxNumberofSensor];
        int sensorsNumber=0;
        try{
            for (int i=0; i < maxNumberofSensor ;i++)
            {
                if (param.equals("all") )
                    sensorsNames[i]=sensoriName[i];
                else
                {
                    if (param.equals("install") && sensori[i]!=null){
                        sensorsNames[sensorsNumber]=sensoriName[i];
                        sensorsNumber=sensorsNumber+1;
                    }
                    if (param.equals("not_install") && sensori[i]==null){
                        sensorsNames[sensorsNumber]=sensoriName[i];
                        sensorsNumber=sensorsNumber+1;
                    }
                }
            }
            String[] result= new String[sensorsNumber];
            for (int x=0; x < sensorsNumber ;x++)
                result[x]=sensorsNames[x];
            jsonObject = new JSONObject();
            jsonObject.put("number",sensorsNumber);
            jsonObject.put("sensors", Arrays.toString(result));

        } catch (JSONException e) {
            e.printStackTrace();
        }finally
        {
            return jsonObject;
        }
    }
    //public  String SensorActiveList()
    public JSONObject SensorActiveList(){
        JSONObject jsonObject=null;
        String[] sensorsNames= new String[maxNumberofSensor];
        int sensorsNumber=0;
        try{
            for (int i=0; i < maxNumberofSensor ;i++)
            {
                if (sensori[i]!=null){
                    sensorsNames[sensorsNumber]=sensoriName[i];
                    sensorsNumber=sensorsNumber+1;
                }
            }
            String[] result= new String[sensorsNumber];
            for (int i=0; i < sensorsNumber ;i++)
            {
                result[i]=sensorsNames[i];
            }
            jsonObject = new JSONObject();
            jsonObject.put("number",sensorsNumber);
            jsonObject.put("sensors", Arrays.toString(result));

        } catch (JSONException e) {
            e.printStackTrace();
        }finally
        {
            return jsonObject;
        }
    }



    public Sensor getSensorByString(String sensorName) {
        Sensor result=null;
        for (int i = 0; i < maxNumberofSensor; i++) {
            if (sensoriName[i].equals(sensorName)) {
                if (sensori[i] != null)
                    result=sensori[i];
            }
        }
        return result;
    }

    public String getSensorActualValueByString(String sensorName)
    {
        String result="";
        for (int i=0; i < maxNumberofSensor ;i++)
        {
            if (sensoriName[i].equals(sensorName)) {
                if (sensoriListener[i] != null)
                    result = sensoriListener[i].getActualValue();
                else
                    result = "NOT INSTALL";
            }
        }
        if (result=="")
            result="NOT FOUND";
        return result;
    }

    public String getSensorActualValueByKey(int sensorKey)
    {
        String result="";
        for (int i=0; i < maxNumberofSensor ;i++)
        {
            if (sensoriKey[i]==sensorKey) {
                if (sensoriListener[i] != null)
                    result = sensoriListener[i].getActualValue();
                else
                    result = "NOT INSTALL";
            }
        }
        if (result=="")
            result="NOT FOUND";
        return result;
    }



    public String castIntToStrSensorType(Integer type)
    {
        String result="";
        if(type==Sensor.TYPE_MAGNETIC_FIELD) result="MAGNETIC_FIELD";
        if(type==Sensor.TYPE_LIGHT) result="LIGHT";
        if(type==Sensor.TYPE_PROXIMITY) result="PROXIMITY";
        if(type==Sensor.TYPE_PRESSURE) result="PRESSURE";
        if(type==Sensor.TYPE_ACCELEROMETER) result="ACCELEROMETER";
        if(type==Sensor.TYPE_AMBIENT_TEMPERATURE) result="AMBIENT_TEMPERATURE";
        if(type==Sensor.TYPE_GYROSCOPE) result="GYROSCOPE";
        if(type==Sensor.TYPE_GRAVITY) result="GRAVITY";
        if(type==Sensor.TYPE_MOTION_DETECT) result="MOTION_DETECT";
        if(type==Sensor.TYPE_RELATIVE_HUMIDITY) result="RELATIVE_HUMIDITY";
        if(type==Sensor.TYPE_STATIONARY_DETECT) result="STATIONARY_DETECT";

        return result;
    }


    public void scanSensors()
    {
        String result="";
        result+="CHECK SENSORI:"+"\n";

        for (int i = 0; i < sensoriKey.length; ++i)
        {
            AscoltatoreSensore sensoreListener;
            Sensor sensore;
            sensore = sensorManager.getDefaultSensor(sensoriKey[i]);
            if (sensore != null) {
                sensori[i] = sensore;
                sensoriListener[i] = new AscoltatoreSensore(sensoriKey[i]);
            }
        }
    }

    public String toString(){


        String result="";
        result="Sensori: \n";
        for (int i = 0; i < sensoriKey.length; ++i) {
            if (sensori[i] != null)
                result+="   OK  ";
            else
                result+="    X  ";
            result+=castIntToStrSensorType(sensoriKey[i]);
            result+="\n";
        }
        return result;
    }

    public void Close()
    {
        for (int i=0; i<maxNumberofSensor;i++)
        {
            sensorManager.unregisterListener(sensoriListener[i]);
            sensoriListener[i]=null;
            sensori[i]=null;
            sensoriKey[i]=0;
        }
        sensorManager=null;
    }

}
