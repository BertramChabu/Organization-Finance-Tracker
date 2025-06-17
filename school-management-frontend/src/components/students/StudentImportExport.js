import React, { useState } from 'react';
import { Button, Container } from '@mui/material';
import API from '../services/api';

const StudentImportExport = ({ schoolId }) => {
  const [file, setFile] = useState(null);

  const handleImport = async () => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await API.post(`schools/${schoolId}/students/import/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Import successful!');
    } catch (error) {
      alert('Import failed: ' + error.message);
    }
  };

  const handleExport = async () => {
    try {
      const response = await API.get(`schools/${schoolId}/students/export/`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'students.xlsx');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      alert('Export failed: ' + error.message);
    }
  };

  return (
    <Container>
      <div>
        <h3>Import Students</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <Button variant="contained" onClick={handleImport}>Import</Button>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h3>Export Students</h3>
        <Button variant="contained" color="secondary" onClick={handleExport}>
          Export to Excel
        </Button>
      </div>
    </Container>
  );
};

export default StudentImportExport;