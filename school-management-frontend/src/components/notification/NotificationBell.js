import React, { useState, useEffect } from 'react';
import { Badge, IconButton, Popover, List, ListItem, ListItemText, Typography } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import API from '../services/api';

const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [anchorEl, setAnchorEl] = useState(null);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await API.get('notifications/');
        setNotifications(response.data);
        setUnreadCount(response.data.filter(n => !n.is_read).length);
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    };
    
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 60000); // Refresh every minute
    
    return () => clearInterval(interval);
  }, []);

  const handleOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
    // Mark as read when closing
    const unreadIds = notifications.filter(n => !n.is_read).map(n => n.id);
    if (unreadIds.length > 0) {
      API.patch('notifications/mark_read/', { ids: unreadIds });
    }
  };

  return (
    <>
      <IconButton color="inherit" onClick={handleOpen}>
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>
      
      <Popover
        open={Boolean(anchorEl)}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <List sx={{ width: 360 }}>
          {notifications.length === 0 ? (
            <ListItem>
              <ListItemText primary="No notifications" />
            </ListItem>
          ) : (
            notifications.map(notification => (
              <ListItem 
                key={notification.id}
                sx={{ 
                  bgcolor: notification.is_read ? 'background.paper' : 'action.selected',
                  borderBottom: '1px solid',
                  borderColor: 'divider'
                }}
              >
                <ListItemText
                  primary={notification.title}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">
                        {notification.message}
                      </Typography>
                      <br />
                      {new Date(notification.created_at).toLocaleString()}
                    </>
                  }
                />
              </ListItem>
            ))
          )}
        </List>
      </Popover>
    </>
  );
};

export default NotificationBell;