import { axiosInstance } from "@/router";

export function setUserRole(role) {
    localStorage.setItem('role', role);
}

export async function getCurentUser(){
    const userResponse = await axiosInstance.get('user/me');
    return userResponse.data;
}



export async function getUserConferences(userId) {
    try{
      const response = await axiosInstance.get('/conferences/all');
      console.log(response.data);
      return response.data.filter(conference => conference.organizer_id === userId);
    }
    catch(error) {
      console.error(error);
      return [];
    }
  }
