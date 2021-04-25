import http from './http-common-servicecall'

class ServiceCall{
    
    submitFiles(files){
        const formData = new FormData();
        console.log(files[0])
        formData.append("file", files[0]);
        formData.append("filename", files[0].name);
        return http.post("/submitFiles", formData, {
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