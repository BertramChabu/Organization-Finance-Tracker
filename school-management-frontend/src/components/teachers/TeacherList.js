import React, { useState, useEffect } from 'react';
import { Table, Button, Container, Spinner, Alert, Form, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import API from '../../services/api';

const TeacherList = ({ schoolId }) => {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        const response = await API.get(`schools/${schoolId}/teachers/`);
        setTeachers(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch teachers');
      } finally {
        setLoading(false);
      }
    };
    fetchTeachers();
  }, [schoolId]);

  const filteredTeachers = teachers.filter(teacher => 
    teacher.user.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    teacher.user.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    teacher.tsc_number?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Teacher Management</h2>
      
      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Control
              type="text"
              placeholder="Search teachers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={6} className="text-end">
          <Button as={Link} to="/teachers/add" variant="success">
            Add New Teacher
          </Button>
        </Col>
      </Row>

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
              <th>TSC No.</th>
              <th>Name</th>
              <th>Subjects</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredTeachers.map(teacher => (
              <tr key={teacher.id}>
                <td>{teacher.tsc_number || 'N/A'}</td>
                <td>{teacher.user.first_name} {teacher.user.last_name}</td>
                <td>
                  {teacher.subjects.map(s => s.name).join(', ')}
                </td>
                <td>
                  <span className={`badge ${teacher.is_active ? 'bg-success' : 'bg-secondary'}`}>
                    {teacher.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <Button 
                    as={Link}
                    to={`/teachers/${teacher.id}`}
                    variant="info" 
                    size="sm"
                  >
                    View
                  </Button>{' '}
                  <Button 
                    as={Link}
                    to={`/teachers/${teacher.id}/edit`}
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

export default TeacherList;