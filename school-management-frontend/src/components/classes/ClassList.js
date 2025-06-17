import React, { useState, useEffect } from 'react';
import { Table, Button, Container, Spinner, Alert, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import API from '../../services/api';

const ClassList = ({ schoolId }) => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await API.get(`schools/${schoolId}/classes/`);
        setClasses(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch classes');
      } finally {
        setLoading(false);
      }
    };
    fetchClasses();
  }, [schoolId]);

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Class Management</h2>
      
      <div className="d-flex justify-content-end mb-3">
        <Button as={Link} to="/classes/add" variant="success">
          Add New Class
        </Button>
      </div>

      {loading ? (
        <div className="text-center">
          <Spinner animation="border" />
        </div>
      ) : error ? (
        <Alert variant="danger">{error}</Alert>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Class Name</th>
              <th>Form</th>
              <th>Stream</th>
              <th>Class Teacher</th>
              <th>Student Count</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {classes.map(cls => (
              <tr key={cls.id}>
                <td>Form {cls.form} {cls.stream.name}</td>
                <td>{cls.form}</td>
                <td>{cls.stream.name}</td>
                <td>
                  {cls.class_teacher 
                    ? `${cls.class_teacher.user.first_name} ${cls.class_teacher.user.last_name}`
                    : 'Not Assigned'}
                </td>
                <td>
                  <Badge bg="primary">{cls.student_count || 0}</Badge>
                </td>
                <td>
                  <Button 
                    as={Link}
                    to={`/classes/${cls.id}`}
                    variant="info" 
                    size="sm"
                  >
                    View
                  </Button>{' '}
                  <Button 
                    as={Link}
                    to={`/classes/${cls.id}/edit`}
                    variant="warning" 
                    size="sm"
                  >
                    Edit
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default ClassList;