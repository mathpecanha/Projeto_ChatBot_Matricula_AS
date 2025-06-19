package com.ibmec.chatbot.repository;

import com.ibmec.chatbot.entity.Matricula;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MatriculaRepository extends JpaRepository<Matricula, Long> {
    
    /**
     * Buscar matrícula por email
     * @param email Email do estudante
     * @return Optional contendo a matrícula se encontrada
     */
    Optional<Matricula> findByEmail(String email);
    
    /**
     * Verificar se existe matrícula com o email informado
     * @param email Email do estudante
     * @return true se existe, false caso contrário
     */
    boolean existsByEmail(String email);
} 