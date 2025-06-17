import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Button, Container, Spinner, Alert, Form } from 'react-bootstrap';
import API from '../../services/api';

const AttendanceForm = ({ date }) => {
  const { classId } = useParams();
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [studentsRes, existingAttendanceRes] = await Promise.all([
          API.get(`classes/${classId}/students/`),
          API.get(`attendance/?date=${date}&class_id=${classId}`)
        ]);
        
        setStudents(studentsRes.data);
        
        // Initialize attendance with existing data if available
        const initialAttendance = {};
        studentsRes.data.forEach(student => {
          const existingRecord = existingAttendanceRes.data.find(
            a => a.student.id === student.id
          );
          initialAttendance[student.id] = existingRecord?.status || 'present';
        });
        setAttendance(initialAttendance);
      } catch (err) {
        setError(err.message || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [classId, date]);

  const handleStatusChange = (studentId, status) => {
    setAttendance(prev => ({
      ...prev,
     