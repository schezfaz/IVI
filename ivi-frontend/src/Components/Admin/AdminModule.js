import React, { useEffect } from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import banner from './ey.png';
import DropzoneComponentAdmin from '../DropComponentAdmin/DropComponentAdmin';
import '../../App.css';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const onDownload = () => {
    const link = document.createElement("a");
    link.download = `download.txt`;
    link.href = "./download.txt";
    link.click();
  };

  const onView= () => {
    const link = document.createElement("a");
    link.download = `download.txt`;
    link.href = "./download.txt";
    link.click();
  };
  
const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    body: {
      fontSize: 14,
    },
  }))(TableCell);
  
  const StyledTableRow = withStyles((theme) => ({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
      },
    },
  }))(TableRow);
  
  function createData(title, guideline) {
    return { title, guideline};
  }
  
  const rows = [
    createData('RISK GUIDELINES', ''),
    createData('IT GUIDELINES', ''),
    createData('AUDIT GUIDELINES', ''),
    createData('COMPLIANCE GUIDELINES', '')
  ];
  
  const useStyles = makeStyles({
    table: {
      minWidth: 500,
    },
  });

function AdminModule() {
    const classes = useStyles(); 
    return (
        <React.Fragment>
            <CssBaseline />
            <AppBar color="default" position="relative">
                <Toolbar>
                    <img src={banner} alt="Banner" width="40" height="50" />
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Typography variant="h6" color="inherit" noWrap>
                        IVI Admin
                    </Typography>
                </Toolbar>
            </AppBar> 

            <Paper>
                <DropzoneComponentAdmin />
            </Paper>    

            <br></br>

            <TableContainer component={Paper} style={{"width" : "40%", "marginLeft" : "30%"}}>
      <Table className={classes.table}  aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>GUIDELINE</StyledTableCell>
            <StyledTableCell >VIEW/DOWNLOAD</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <StyledTableRow key={row.title}>
              <StyledTableCell component="th" scope="row">
                {row.title}
              </StyledTableCell>
              <StyledTableCell >
              <Button onClick={onView} variant="contained" style={{backgroundColor:"#ffe600"}}>
                View
              </Button>
              &nbsp;&nbsp;&nbsp;
                <Button onClick={onDownload} variant="contained" style={{backgroundColor:"#ffe600"}}>
                  Download
                </Button>
                
                </StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>

           
    </React.Fragment> 
  )
}

export default AdminModule;