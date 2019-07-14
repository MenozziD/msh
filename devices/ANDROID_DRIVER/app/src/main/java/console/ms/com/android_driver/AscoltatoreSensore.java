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

    public AscoltatoreSensore(Integer type, TextView tv)
    {
        String um="";
        sensorType=type;
        if (sensorType==Sensor.TYPE_LIGHT) um="lx";
        if (sensorType==Sensor.TYPE_AMBIENT_TEMPERATURE) um="°C";
        if (sensorType==Sensor.TYPE_PRESSURE) um="°bar";
        sensorUM=um;
        sensorTextViewOut=tv;
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        float value = event.values[0];
        sensorTextViewOut.setText(Float.toString(value)+sensorUM);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}
