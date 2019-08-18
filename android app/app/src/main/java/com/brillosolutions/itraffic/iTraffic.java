package com.brillosolutions.itraffic;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.*;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.*;

import java.io.*;
import java.net.*;

public class iTraffic extends AppCompatActivity
{
    private EditText myID, myPassword;
    private String usrID, usrPassword;
    private Intent mapsActivity;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_i_traffic);
        myID = (EditText) findViewById(R.id.editText2);
        myPassword = (EditText) findViewById(R.id.editText);
    }

    public void btnClick(View v)
    {
        usrID = myID.getText().toString();
        usrPassword = myPassword.getText().toString();
        if(!usrID.equals("") && !usrPassword.equals(""))
        {
            if(usrID.length() == 4)
            {
                Thread txThread = new Thread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        try
                        {
                            String instanceLink = "http://intelights-api.anukai.com:8080/crossing/userLogin.php";
                            URL url = new URL(instanceLink);
                            URLConnection urlConnection = url.openConnection();
                            urlConnection.setDoOutput(true);
                            PrintStream postMan = new PrintStream(urlConnection.getOutputStream());
                            postMan.print("&id=" + usrID);
                            BufferedReader serverEcho = new BufferedReader
                                    (new InputStreamReader(urlConnection.getInputStream()));
                            String msgLine, homeReply = "";
                            while ((msgLine = serverEcho.readLine()) != null)
                                homeReply += msgLine;
                            serverEcho.close();
                            Message rxdPswd = Message.obtain();
                            rxdPswd.obj = homeReply;
                            mHandler.sendMessage(rxdPswd);
                        }
                        catch (Exception ignored) {}
                    }
                });txThread.start();
            }
            else
            {
                Toast.makeText(this, "Type correct user ID!", Toast.LENGTH_SHORT).show();
            }
        }
        else
        {
            Toast.makeText(this, "Type your credentials!", Toast.LENGTH_SHORT).show();
        }
    }
    @SuppressLint("HandlerLeak")
    Handler mHandler = new Handler()
    {
        private String rxdReply;
        @Override
        public void handleMessage(Message rxdMsg)
        {
            rxdReply = rxdMsg.obj.toString().trim();
            super.handleMessage(rxdMsg);
            String[] breakReply = rxdReply.split(",");
            if(breakReply[0].equals(myPassword.getText().toString()))
            {
                mapsActivity = new Intent(iTraffic.this, Select.class);
                mapsActivity.putExtra("id", usrID);
                mapsActivity.putExtra("lat", breakReply[1]);
                mapsActivity.putExtra("lon", breakReply[2]);
                startActivity(mapsActivity);
                Toast.makeText(iTraffic.this, "You have signed in.", Toast.LENGTH_SHORT).show();
            }
            else
            {
                Toast.makeText(iTraffic.this, "Wrong credentials or user not exists!", Toast.LENGTH_SHORT).show();
            }
        }
    };
}
