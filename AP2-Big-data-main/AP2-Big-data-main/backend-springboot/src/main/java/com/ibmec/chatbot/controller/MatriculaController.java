package com.ibmec.chatbot.controller;

import com.ibmec.chatbot.dto.MatriculaRequestDTO;
import com.ibmec.chatbot.dto.MatriculaResponseDTO;
import com.ibmec.chatbot.service.MatriculaService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/matriculas")
@CrossOrigin(origins = "*") // Permitir CORS para o bot
public class MatriculaController {

    private static final Logger logger = LoggerFactory.getLogger(MatriculaController.class);

    @Autowired
    private MatriculaService matriculaService;

    /**
     * Endpoint principal: POST /api/matriculas
     * Criar uma nova matrícula
     */
    @PostMapping
    public ResponseEntity<?> criarMatricula(@Valid @RequestBody MatriculaRequestDTO requestDTO, 
                                          BindingResult bindingResult) {
        logger.info("Recebida solicitação de matrícula: {}", requestDTO);

        // Verificar erros de validação
        if (bindingResult.hasErrors()) {
            Map<String, String> errors = new HashMap<>();
            bindingResult.getFieldErrors().forEach(error -> 
                errors.put(error.getField(), error.getDefaultMessage())
            );
            
            logger.warn("Erro de validação na matrícula: {}", errors);
            return ResponseEntity.badRequest().body(Map.of("errors", errors));
        }

        try {
            MatriculaResponseDTO response = matriculaService.criarMatricula(requestDTO);
            logger.info("Matrícula criada com sucesso: ID = {}", response.getId());
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
            
        } catch (IllegalArgumentException e) {
            logger.warn("Erro ao criar matrícula: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(Map.of("error", e.getMessage()));
                    
        } catch (Exception e) {
            logger.error("Erro interno ao criar matrícula", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Erro interno do servidor"));
        }
    }

    /**
     * Listar todas as matrículas
     */
    @GetMapping
    public ResponseEntity<List<MatriculaResponseDTO>> listarMatriculas() {
        logger.info("Listando todas as matrículas");
        
        try {
            List<MatriculaResponseDTO> matriculas = matriculaService.listarMatriculas();
            return ResponseEntity.ok(matriculas);
            
        } catch (Exception e) {
            logger.error("Erro ao listar matrículas", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Buscar matrícula por ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<?> buscarMatriculaPorId(@PathVariable Long id) {
        logger.info("Buscando matrícula por ID: {}", id);
        
        try {
            Optional<MatriculaResponseDTO> matricula = matriculaService.buscarMatriculaPorId(id);
            
            if (matricula.isPresent()) {
                return ResponseEntity.ok(matricula.get());
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("error", "Matrícula não encontrada"));
            }
            
        } catch (Exception e) {
            logger.error("Erro ao buscar matrícula por ID", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Erro interno do servidor"));
        }
    }

    /**
     * Buscar matrícula por email
     */
    @GetMapping("/email/{email}")
    public ResponseEntity<?> buscarMatriculaPorEmail(@PathVariable String email) {
        logger.info("Buscando matrícula por email: {}", email);
        
        try {
            Optional<MatriculaResponseDTO> matricula = matriculaService.buscarMatriculaPorEmail(email);
            
            if (matricula.isPresent()) {
                return ResponseEntity.ok(matricula.get());
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("error", "Matrícula não encontrada"));
            }
            
        } catch (Exception e) {
            logger.error("Erro ao buscar matrícula por email", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Erro interno do servidor"));
        }
    }

    /**
     * Endpoint de teste para verificar se a API está funcionando
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "message", "API de Matrículas está funcionando",
                "timestamp", java.time.LocalDateTime.now().toString()
        ));
    }
} 