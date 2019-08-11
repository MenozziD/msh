package console.ms.com.android_driver;

import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.widget.TextView;

public class SensorsOnBoard  {

    private Sensor[] sensori;
    public Sensor[] getsensori(){return sensori;}

    private Integer[] sensoriKey;
    public Integer[] getsensoriKey(){return sensoriKey;}

    private AscoltatoreSensore[] sensoriListener;
    public AscoltatoreSensore[] getsensoriListener(){return sensoriListener;}

    private ServizioADTW servizio;
    private SensorManager sensorManager;

    static final Integer maxNumberofSensor = 8;

    public SensorsOnBoard (ServizioADTW servizio)
    {
        this.servizio= servizio;
        sensorManager = (SensorManager) servizio.getSystemService(servizio.SENSOR_SERVICE);
        sensoriKey= new Integer[maxNumberofSensor];
        sensori= new Sensor[maxNumberofSensor];
        sensoriListener = new AscoltatoreSensore[maxNumberofSensor];
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
        }

        scanSensors();

        for (int i=0; i<maxNumberofSensor;i++) {
            if (getsensori()[i] != null)
                sensorManager.registerListener(getListenerSensore(i), getSensore(i), SensorManager.SENSOR_DELAY_FASTEST);
        }

    }

    public Sensor getSensore (Integer position)
    {
        return sensori[position];
    }

    public AscoltatoreSensore getListenerSensore (Integer position) { return sensoriListener[position];}

    public AscoltatoreSensore getListenerSensoreByType (Integer type) {
        Integer position=-1;
        for (int i =0; i < maxNumberofSensor ;i++)
            if (type==sensoriKey[i]) position= i;
        return getListenerSensore(position);
    }


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
            sensorManager.unregisterListener(getListenerSensore(i));
            sensoriListener[i]=null;
            sensori[i]=null;
            sensoriKey[i]=0;
        }
        sensorManager=null;
        servizio=null;
    }

}
