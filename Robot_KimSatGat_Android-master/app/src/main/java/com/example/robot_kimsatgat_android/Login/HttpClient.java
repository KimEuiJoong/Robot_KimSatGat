package com.example.robot_kimsatgat_android.Login;

import android.util.Log;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class HttpClient {

    private static Retrofit retrofit;
    private static OkHttpClient client;

    // Http 통신을 위한 Retrofit 객체반환
    public static Retrofit getRetrofit() {
        if(client == null){
            client = new OkHttpClient.Builder().addInterceptor(httpLoggingInterceptor()).build();
        }
        if( retrofit == null )
        {
            Retrofit.Builder builder = new Retrofit.Builder();
            builder.baseUrl( "https://rest.robotkimsatgat.p-e.kr" );
            builder.addConverterFactory( GsonConverterFactory.create() );  // 받아오는 Json 구조의 데이터를 객체 형태로 변환
            builder.client(client);

            retrofit = builder.build();
        }

        return retrofit;
    }

    //로그 남기기 위한 부분.
    private static HttpLoggingInterceptor httpLoggingInterceptor(){
        HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor(new HttpLoggingInterceptor.Logger() {
            @Override
            public void log(String message) {
                Log.w("http_log:",message);
            }
        });
        return interceptor.setLevel(HttpLoggingInterceptor.Level.BODY);
    }
}
