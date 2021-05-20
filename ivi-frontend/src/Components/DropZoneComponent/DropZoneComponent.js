import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import ServiceCall from '../../Service/ServiceCall';
//import { Document, Page } from 'react-pdf';

const baseStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 2,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  transition: 'border .3s ease-in-out'
};

const activeStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676'
};

const rejectStyle = {
  borderColor: '#ff1744'
};

function DropzoneComponent(props) {
  const [files, setFiles] = useState([]);
  // const [returnFile, setReturnFile] = useState();
  // const [numPages, setNumPages] = useState(null);
  // const [pageNumber, setPageNumber] = useState(1);

  const onDrop = useCallback(acceptedFiles => {
    setFiles(acceptedFiles.map(file => Object.assign(file, {
      preview: URL.createObjectURL(file)
    })));
  }, []);

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject
  } = useDropzone({
    onDrop,
    // accept: 'image/jpeg, image/png, file/pdf'
  });

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }), [
    isDragActive,
    isDragReject,
    isDragAccept
  ]);

  const thumbs = files.map(file => (
    <div key={file.name}>
      {/* <img
        src={file.preview}
        alt={file.name}
      /> */}
      <Typography variant="h5" align="center" color="textSecondary" paragraph>
        <i>{file.name}</i>
      </Typography>
       {/* <div>{file.name}</div> */}
    </div>
  ));

  // clean up
  useEffect(() => () => {
    files.forEach(file => URL.revokeObjectURL(file.preview));
  }, [files]);

  // function onDocumentLoadSuccess({ numPages }) {
  //   setNumPages(numPages);
  // }

  function submitFiles(){
    const formData = new FormData()
    formData.append("file", files[0]);
    formData.append("filename", files[0].name);
    formData.append("brandGuideline", localStorage.getItem("brandGuideline"));
    ServiceCall.submitFile(formData).then((response)=>{
      console.log(response.data)
      alert(response.data)
    })
  }

  return (
    <section>
      <div {...getRootProps({style})}>
        <input {...getInputProps()} />
        <div><b>Drag and drop your documents here</b></div>
      </div>
      <br/>
      <aside>
        {thumbs}
      </aside>
      <br/>
      <Button variant="contained" style={{backgroundColor:"#ffe600"}} onClick={()=> submitFiles()}>
        Apply IVI Now
      </Button>
      <br/><br/>

      {/* {returnFile && <Document
        file={returnFile}
        onLoadSuccess={onDocumentLoadSuccess}
      >
        <Page pageNumber={pageNumber} />
      </Document>}
      <p>Page {pageNumber} of {numPages}</p> */}


    </section>

    
  )
}

export default DropzoneComponent;