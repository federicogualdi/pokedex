package com.federicogualdi.pokemon.pokedex.rest.em;

import com.federicogualdi.pokemon.pokedex.rest.dto.ErrorDto;

import javax.ws.rs.core.Response.Status;

public enum ErrorCollection {
    NOT_FOUND_EXCEPTION(new ErrorDto.Builder()
            .title("Pokemon not found")
            .status(Status.NOT_FOUND.getStatusCode()).build()),
    BAD_REQUEST_EXCEPTION(new ErrorDto.Builder()
            .title("Bad request")
            .status(Status.BAD_REQUEST.getStatusCode()).build()),
    CLIENT_REST_ERROR_EXCEPTION(new ErrorDto.Builder()
            .title("Client Rest Server Error")
            .status(Status.SERVICE_UNAVAILABLE.getStatusCode()).build()),
    INTERNAL_SERVER_ERROR_EXCEPTION(new ErrorDto.Builder()
            .title("Internal Server Error")
            .status(Status.INTERNAL_SERVER_ERROR.getStatusCode()).build()),
    ;
    private final ErrorDto error;

    public ErrorDto getError() {
        return error;
    }

    ErrorCollection(final ErrorDto error) {
        this.error = error;
    }
}
