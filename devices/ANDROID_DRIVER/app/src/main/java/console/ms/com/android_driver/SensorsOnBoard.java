package console.ms.com.android_driver;

import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.widget.TextView;

public class SensorsOnBoard  {

    private Sensor[] sensori;
    private Integer[] sensoriKey;
    private AscoltatoreSensore[] sensoriListener;
    private TextView[] sensoriTextView;
    private Boolean[] sensoriFlagInstall;

    private SensorManager sensorManager;

    static final Integer maxNumberofSensor =3;

    public SensorsOnBoard (SensorManager pSensorManager,TextView[] pTextView )
    {
        sensorManager=pSensorManager;
        sensoriTextView= new TextView[maxNumberofSensor];
        sensoriTextView=pTextView;
        sensoriKey= new Integer[maxNumberofSensor];
        sensori= new Sensor[maxNumberofSensor];
        sensoriListener = new AscoltatoreSensore[maxNumberofSensor];
        sensoriFlagInstall = new Boolean[maxNumberofSensor];


        for (int i =0; i < maxNumberofSensor ;i++)
        {
            if (i==0)  sensoriKey[i] = Sensor.TYPE_MAGNETIC_FIELD;
            if (i==1)  sensoriKey[i] = Sensor.TYPE_LIGHT;
            if (i==2)  sensoriKey[i] = Sensor.TYPE_PROXIMITY;

            sensoriFlagInstall[i]=false;
        }
    }

    public Sensor getSensore (Integer position)
    {
        return sensori[position];
    }

    public AscoltatoreSensore getListenerSensore (Integer position) { return sensoriListener[position];}

    public AscoltatoreSensore getListenerSensoreByType (Integer type) {

        Integer position=-1;

        if (type==Sensor.TYPE_MAGNETIC_FIELD) position= 0;
        if (type==Sensor.TYPE_LIGHT) position= 1;
        if (type==Sensor.TYPE_PROXIMITY) position= 2;

        return getListenerSensore(position);
    }

    /*
    public String castIntToStrSensorType(Integer type)
    {
        String result="";
        if(type==Sensor.TYPE_MAGNETIC_FIELD) result="TYPE_MAGNETIC_FIELD";
        if(type==Sensor.TYPE_LIGHT) result="TYPE_LIGHT";
        if(type==Sensor.TYPE_PROXIMITY) result="TYPE_PROXIMITY";

        if(type==Sensor.TYPE_PRESSURE) result="TYPE_PRESSURE";
        if(type==Sensor.TYPE_ACCELEROMETER) result="TYPE_ACCELEROMETER";
        if(type==Sensor.TYPE_AMBIENT_TEMPERATURE) result="TYPE_AMBIENT_TEMPERATURE";
        if(type==Sensor.TYPE_GYROSCOPE) result="TYPE_GYROSCOPE";
        if(type==Sensor.TYPE_GRAVITY) result="TYPE_GRAVITY";

        return result;
    }
*/

    public void scanSensors()
    {
        String result="";
        result+="CHECK SENSORI:"+"\n";

        for (int i = 0; i < sensoriKey.length; ++i)
        {
            AscoltatoreSensore sensoreListener;
            Sensor sensore;
            sensore = sensorManager.getDefaultSensor(sensoriKey[i]);
            if (sensore != null)
            {
                sensori[i]=sensore;
                sensoreListener = new AscoltatoreSensore(sensoriKey[i],sensoriTextView[i]);
                sensoriListener[i]=sensoreListener;
                sensoriFlagInstall[i]=true;
            }
            else {
                sensoriFlagInstall[i]=false;
                sensoriTextView[i].setText("NOT INSTALL");
            }
        }
    }


}
