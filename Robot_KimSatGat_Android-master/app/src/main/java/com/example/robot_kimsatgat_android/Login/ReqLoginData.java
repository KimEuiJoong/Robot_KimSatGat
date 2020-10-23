package com.example.robot_kimsatgat_android.Login;

import com.google.gson.annotations.Expose;

// api/login 요청 데이터
public class ReqLoginData {
    @Expose //if its null, skip this entity
            String idToken;

    public ReqLoginData(String idToken){
        this.idToken = idToken;
    }

    @Override
    public String toString(){
        return "token="+idToken;
    }
}
