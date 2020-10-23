package com.example.robot_kimsatgat_android.Login;

import com.google.gson.annotations.Expose;

import androidx.annotation.NonNull;

// api/login 응답 데이터
public class ResLoginData {

    @Expose
    String token;

    @NonNull
    @Override
    public String toString() {
        return "[ResLoginData] token=" + token;
    }
}
