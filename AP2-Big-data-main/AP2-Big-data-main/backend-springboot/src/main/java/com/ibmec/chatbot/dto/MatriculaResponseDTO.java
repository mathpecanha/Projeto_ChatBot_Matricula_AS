package com.ibmec.chatbot.dto;

import com.ibmec.chatbot.entity.Matricula;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class MatriculaResponseDTO {

    private Long id;
    private String nome;
    private String email;
    private String curso;
    private String dataMatricula;
    private String message;

    public MatriculaResponseDTO() {}

    public MatriculaResponseDTO(Matricula matricula, String message) {
        this.id = matricula.getId();
        this.nome = matricula.getNome();
        this.email = matricula.getEmail();
        this.curso = matricula.getCurso();
        this.dataMatricula = matricula.getDataMatricula().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        this.message = message;
    }

    public MatriculaResponseDTO(Long id, String nome, String email, String curso, LocalDateTime dataMatricula, String message) {
        this.id = id;
        this.nome = nome;
        this.email = email;
        this.curso = curso;
        this.dataMatricula = dataMatricula.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        this.message = message;
    }

    // Getters e Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getCurso() {
        return curso;
    }

    public void setCurso(String curso) {
        this.curso = curso;
    }

    public String getDataMatricula() {
        return dataMatricula;
    }

    public void setDataMatricula(String dataMatricula) {
        this.dataMatricula = dataMatricula;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return "MatriculaResponseDTO{" +
                "id=" + id +
                ", nome='" + nome + '\'' +
                ", email='" + email + '\'' +
                ", curso='" + curso + '\'' +
                ", dataMatricula='" + dataMatricula + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
} 