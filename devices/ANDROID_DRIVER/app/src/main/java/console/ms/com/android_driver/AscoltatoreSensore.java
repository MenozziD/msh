package console.ms.com.android_driver;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.widget.TextView;

public class AscoltatoreSensore  implements SensorEventListener {

    private Integer sensorType;
    private String sensorUM;
    private TextView sensorTextViewOut;
    private String sensorActualValue;

    public AscoltatoreSensore(Integer type, TextView tv)
    {
        sensorActualValue="";
        sensorType=type;
        if (sensorType==Sensor.TYPE_LIGHT) sensorUM=" lx";
        if (sensorType==Sensor.TYPE_AMBIENT_TEMPERATURE) sensorUM=" °C";
        if (sensorType==Sensor.TYPE_PRESSURE) sensorUM=" bar";
        if (sensorType==Sensor.TYPE_PROXIMITY) sensorUM="";
        if (sensorType==Sensor.TYPE_MAGNETIC_FIELD) sensorUM="";
        sensorTextViewOut=tv;
    }

    public String getActualValue()
    {
        return sensorActualValue;
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        sensorActualValue = Float.toString(event.values[0])+sensorUM;
        sensorTextViewOut.setText(sensorActualValue);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}
