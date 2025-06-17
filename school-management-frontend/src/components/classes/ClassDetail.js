import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Container, Tab, Tabs, Spinner, Alert, Table, Badge, ListGroup } from 'react-bootstrap';
import API from '../../services/api';

const ClassDetail = () => {
  const { id } = useParams();
  const [classData, setClassData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('students');

  useEffect(() => {
    const fetchClassData = async () => {
      try {
        const response = await API.get(`classes/${id}/`);
        setClassData(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch class data');
      } finally {
        setLoading(false);
      }
    };
    fetchClassData();
  }, [id]);

  if (loading) return <Spinner animation="border" className="d-block mx-auto mt-5" />;
  if (error) return <Alert variant="danger" className="mt-4">{error}</Alert>;
  if (!classData) return null;

  return (
    <Container className="mt-4">
      <Card className="shadow">
        <Card.Body>
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h2>Form {classData.form} {classData.stream.name}</h2>
            <Badge bg="primary" pill>
              {classData.student_count} Students
            </Badge>
          </div>

          <div className="mb-4">
            <p><strong>Class Teacher:</strong> {classData.class_teacher 
              ? `${classData.class_teacher.user.first_name} ${classData.class_teacher.user.last_name}`
              : 'Not assigned'}</p>
          </div>

          <Tabs
            activeKey={activeTab}
            onSelect={(k) => setActiveTab(k)}
            className="mb-4"
          >
            <Tab eventKey="students" title="Students">
              <div className="mt-4">
                <h5>Students in this Class</h5>
                {classData.students.length > 0 ? (
                  <Table striped bordered hover>
                    <thead>
                      <tr>
                        <th>Admission No.</th>
                        <th>Name</th>
                        <th>Gender</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {classData.students.map(student => (
                        <tr key={student.id}>
                          <td>{student.admission_number}</td>
                          <td>{student.user.first_name} {student.user.last_name}</td>
                          <td>{student.gender === 'M' ? 'Male' : 'Female'}</td>
                          <td>
                            <Badge bg={student.is_active ? 'success' : 'secondary'}>
                              {student.is_active ? 'Active' : 'Inactive'}
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                ) : (
                  <Alert variant="info">No students in this class</Alert>
                )}
              </div>
            </Tab>
            <Tab eventKey="subjects" title="Subjects">
              <div className="mt-4">
                <h5>Subjects Offered</h5>
                {classData.subjects.length > 0 ? (
                  <ListGroup>
                    {classData.subjects.map(subject => (
                      <ListGroup.Item key={subject.id}>
                        {subject.name} ({subject.code})
                      </ListGroup.Item>
                    ))}
                  </ListGroup>
                ) : (
                  <Alert variant="info">No subjects assigned to this class</Alert>
                )}
              </div>
            </Tab>
            <Tab eventKey="teachers" title="Teachers">
              <div className="mt-4">
                <h5>Subject Teachers</h5>
                {classData.subject_teachers.length > 0 ? (
                  <Table striped bordered hover>
                    <thead>
                      <tr>
                        <th>Subject</th>
                        <th>Teacher</th>
                      </tr>
                    </thead>
                    <tbody>
                      {classData.subject_teachers.map(item => (
                        <tr key={item.subject.id}>
                          <td>{item.subject.name}</td>
                          <td>{item.teacher.user.first_name} {item.teacher.user.last_name}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                ) : (
                  <Alert variant="info">No teachers assigned to this class</Alert>
                )}
              </div>
            </Tab>
          </Tabs>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ClassDetail;