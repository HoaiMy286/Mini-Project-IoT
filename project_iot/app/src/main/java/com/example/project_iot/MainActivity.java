package com.example.project_iot;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {

    MQTTHelper mqttHelper;

    TextView textHUMI, textTEMP, textMOISTURE, textAI;
    LabeledSwitch buttonLED, buttonPUMP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textAI = findViewById(R.id.textAI);

        textHUMI = findViewById(R.id.textHUMI);
        textTEMP = findViewById(R.id.textTEMP);
        textMOISTURE = findViewById(R.id.textMOISTURE);

        buttonLED = findViewById(R.id.buttonLED);
        buttonPUMP = findViewById(R.id.buttonPUMP);

        buttonLED.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn){
                    sendDataMQTT("MTPQ_BKU/feeds/led", "1");
                } else {
                    sendDataMQTT("MTPQ_BKU/feeds/led", "0");
                }
            }
        });
        buttonPUMP.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn){
                    sendDataMQTT("MTPQ_BKU/feeds/pump", "1");
                } else {
                    sendDataMQTT("MTPQ_BKU/feeds/pump", "0");
                }
            }
        });

        startMQTT();
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
            throw new RuntimeException(e);
        }
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                if(topic.contains("humidity")){
                    textHUMI.setText(message.toString() + "%");
                } else if (topic.contains("temperature")) {
                    textTEMP.setText(message.toString() + "°C");
                }else if (topic.contains("soil-moisture")) {
                    textMOISTURE.setText(message.toString() + "%");
                }else if (topic.contains("ai")) {
                    textAI.setText(message.toString());
                }else if (topic.contains("led")) {
                    if(message.toString().equals("1")){
                        buttonLED.setOn(true);
                    } else {
                        buttonLED.setOn(false);
                    }
                } else if (topic.contains("pump")) {
                    if(message.toString().equals("1")){
                        buttonPUMP.setOn(true);
                    } else {
                        buttonPUMP.setOn(false);
                    }
                }

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}