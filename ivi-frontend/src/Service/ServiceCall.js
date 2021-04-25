import http from './http-common-servicecall'

class ServiceCall{
    
    submitFile(files){
        const formData = new FormData();
        console.log(files[0])
        formData.append("file", files[0]);
        formData.append("filename", files[0].name);
        return http.post("/submitFile", formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        })
    }

    returnFile(){
        return http.post("/returnFile", {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        })
    }


    // signUp(userLoginDetails){
    //     return http.post("/signUp", userLoginDetails, {
    //         headers: {
    //             "Content-Type": "multipart/form-data"
    //         }
    //     });
    // }
}

export default new ServiceCall();