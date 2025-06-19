package com.ibmec.chatbot.service;

import com.ibmec.chatbot.dto.MatriculaRequestDTO;
import com.ibmec.chatbot.dto.MatriculaResponseDTO;
import com.ibmec.chatbot.entity.Matricula;
import com.ibmec.chatbot.repository.MatriculaRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class MatriculaService {

    private static final Logger logger = LoggerFactory.getLogger(MatriculaService.class);

    @Autowired
    private MatriculaRepository matriculaRepository;

    /**
     * Criar uma nova matrícula
     * @param requestDTO Dados da matrícula
     * @return DTO de resposta com dados da matrícula criada
     * @throws IllegalArgumentException se já existe matrícula com o email
     */
    public MatriculaResponseDTO criarMatricula(MatriculaRequestDTO requestDTO) {
        logger.info("Criando nova matrícula para: {} - {}", requestDTO.getNome(), requestDTO.getEmail());

        // Verificar se já existe matrícula com o mesmo email
        if (matriculaRepository.existsByEmail(requestDTO.getEmail())) {
            throw new IllegalArgumentException("Já existe uma matrícula cadastrada com este email: " + requestDTO.getEmail());
        }

        // Criar nova matrícula
        Matricula matricula = new Matricula(
                requestDTO.getNome(),
                requestDTO.getEmail(),
                requestDTO.getCurso()
        );

        // Salvar no banco de dados
        Matricula matriculaSalva = matriculaRepository.save(matricula);

        logger.info("Matrícula criada com sucesso: ID = {}", matriculaSalva.getId());

        return new MatriculaResponseDTO(matriculaSalva, "Matrícula realizada com sucesso!");
    }

    /**
     * Listar todas as matrículas
     * @return Lista de DTOs de resposta
     */
    public List<MatriculaResponseDTO> listarMatriculas() {
        logger.info("Listando todas as matrículas");

        List<Matricula> matriculas = matriculaRepository.findAll();

        return matriculas.stream()
                .map(matricula -> new MatriculaResponseDTO(matricula, null))
                .collect(Collectors.toList());
    }

    /**
     * Buscar matrícula por ID
     * @param id ID da matrícula
     * @return DTO de resposta ou Optional vazio se não encontrada
     */
    public Optional<MatriculaResponseDTO> buscarMatriculaPorId(Long id) {
        logger.info("Buscando matrícula por ID: {}", id);

        Optional<Matricula> matricula = matriculaRepository.findById(id);

        return matricula.map(m -> new MatriculaResponseDTO(m, null));
    }

    /**
     * Buscar matrícula por email
     * @param email Email do estudante
     * @return DTO de resposta ou Optional vazio se não encontrada
     */
    public Optional<MatriculaResponseDTO> buscarMatriculaPorEmail(String email) {
        logger.info("Buscando matrícula por email: {}", email);

        Optional<Matricula> matricula = matriculaRepository.findByEmail(email);

        return matricula.map(m -> new MatriculaResponseDTO(m, null));
    }

    /**
     * Verificar se existe matrícula com o email
     * @param email Email do estudante
     * @return true se existe, false caso contrário
     */
    public boolean existeMatriculaComEmail(String email) {
        return matriculaRepository.existsByEmail(email);
    }
} 