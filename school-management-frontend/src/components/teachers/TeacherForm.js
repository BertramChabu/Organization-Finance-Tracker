import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Button, Container, Alert, Spinner, Card, Row, Col } from 'react-bootstrap';
import API from '../../services/api';

const TeacherForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [formData, setFormData] = useState({
    user: {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: ''
    },
    tsc_number: '',
    subjects: [],
    is_active: true,
    date_hired: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [subjectsRes] = await Promise.all([
          API.get('subjects/')
        ]);
        setSubjects(subjectsRes.data);

        if (id) {
          const teacherRes = await API.get(`teachers/${id}/`);
          setFormData(teacherRes.data);
        }
      } catch (err) {
        setError(err.message || 'Failed to fetch data');
      }
    };
    fetchData();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (id) {
        await API.put(`teachers/${id}/`, formData);
      } else {
        await API.post('teachers/', formData);
      }
      navigate('/teachers');
    } catch (err) {
      setError(err.response?.data || err.message || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSubjectChange = (subjectId, isChecked) => {
    setFormData(prev => {
      const newSubjects = isChecked 
        ? [...prev.subjects, subjectId]
        : prev.subjects.filter(id => id !== subjectId);
      return { ...prev, subjects: newSubjects };
    });
  };

  return (
    <Container className="mt-4">
      <Card className="shadow">
        <Card.Body>
          <h2 className="mb-4">{id ? 'Edit' : 'Add'} Teacher</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          
          <Form onSubmit={handleSubmit}>
            <h5 className="mt-4 mb-3">Personal Information</h5>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>First Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.user.first_name}
                    onChange={(e) => setFormData({
                      ...formData,
                      user: {...formData.user, first_name: e.target.value}
                    })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Last Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.user.last_name}
                    onChange={(e) => setFormData({
                      ...formData,
                      user: {...formData.user, last_name: e.target.value}
                    })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.user.username}
                    onChange={(e) => setFormData({
                      ...formData,
                      user: {...formData.user, username: e.target.value}
                    })}
                    required
                    disabled={!!id}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={formData.user.email}
                    onChange={(e) => setFormData({
                      ...formData,
                      user: {...formData.user, email: e.target.value}
                    })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            {!id && (
              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  value={formData.user.password}
                  onChange={(e) => setFormData({
                    ...formData,
                    user: {...formData.user, password: e.target.value}
                  })}
                  required={!id}
                />
              </Form.Group>
            )}

            <h5 className="mt-4 mb-3">Professional Information</h5>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>TSC Number</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.tsc_number}
                    onChange={(e) => setFormData({
                      ...formData,
                      tsc_number: e.target.value
                    })}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Date Hired</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.date_hired}
                    onChange={(e) => setFormData({
                      ...formData,
                      date_hired: e.target.value
                    })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Subjects</Form.Label>
              <div className="d-flex flex-wrap gap-3">
                {subjects.map(subject => (
                  <Form.Check
                    key={subject.id}
                    type="checkbox"
                    id={`subject-${subject.id}`}
                    label={subject.name}
                    checked={formData.subjects.includes(subject.id)}
                    onChange={(e) => handleSubjectChange(subject.id, e.target.checked)}
                  />
                ))}
              </div>
            </Form.Group>

            <Form.Check
              type="switch"
              id="is-active-switch"
              label="Active Teacher"
              checked={formData.is_active}
              onChange={(e) => setFormData({
                ...formData,
                is_active: e.target.checked
              })}
            />

            <div className="mt-4">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? <Spinner size="sm" /> : 'Save Teacher'}
              </Button>{' '}
              <Button variant="secondary" onClick={() => navigate('/teachers')}>
                Cancel
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default TeacherForm;