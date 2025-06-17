import React, { useState } from 'react';
import { Button, Menu, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, Select, FormControl, InputLabel } from '@mui/material';
import API from '../services/api';

const BulkActions = ({ schoolId, selectedStudents, refreshData }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [action, setAction] = useState('');
  const [classId, setClassId] = useState('');
  const [classes, setClasses] = useState([]);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleDialogOpen = (actionType) => {
    setAction(actionType);
    if (actionType === 'assign_class') {
      API.get(`schools/${schoolId}/classes/`).then(response => {
        setClasses(response.data);
      });
    }
    setDialogOpen(true);
    handleMenuClose();
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
  };

  const executeBulkAction = () => {
    API.post(`schools/${schoolId}/students/bulk_actions/`, {
      action: action,
      student_ids: selectedStudents,
      class_id: classId
    }).then(() => {
      refreshData();
      handleDialogClose();
    });
  };

  return (
    <div>
      <Button 
        variant="contained" 
        onClick={handleMenuOpen}
        disabled={selectedStudents.length === 0}
      >
        Bulk Actions ({selectedStudents.length})
      </Button>
      
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleDialogOpen('promote')}>Promote</MenuItem>
        <MenuItem onClick={() => handleDialogOpen('deactivate')}>Deactivate</MenuItem>
        <MenuItem onClick={() => handleDialogOpen('assign_class')}>Assign to Class</MenuItem>
      </Menu>
      
      <Dialog open={dialogOpen} onClose={handleDialogClose}>
        <DialogTitle>
          {action === 'promote' && 'Promote Students'}
          {action === 'deactivate' && 'Deactivate Students'}
          {action === 'assign_class' && 'Assign Students to Class'}
        </DialogTitle>
        <DialogContent>
          {action === 'assign_class' && (
            <FormControl fullWidth>
              <InputLabel>Class</InputLabel>
              <Select
                value={classId}
                onChange={(e) => setClassId(e.target.value)}
                label="Class"
              >
                {classes.map(cls => (
                  <MenuItem key={cls.id} value={cls.id}>
                    Form {cls.form} {cls.stream.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
          {action === 'promote' && (
            <p>Are you sure you want to promote {selectedStudents.length} students?</p>
          )}
          {action === 'deactivate' && (
            <p>Are you sure you want to deactivate {selectedStudents.length} students?</p>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Cancel</Button>
          <Button onClick={executeBulkAction} color="primary">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default BulkActions;