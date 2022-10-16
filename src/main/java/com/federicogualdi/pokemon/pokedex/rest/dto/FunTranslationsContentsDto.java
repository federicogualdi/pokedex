package com.federicogualdi.pokemon.pokedex.rest.dto;

public class FunTranslationsContentsDto {
    private String translated;

    public String getTranslated() {
        return translated.trim().replaceAll(" +", " ");
    }

    @Override
    public String toString() {
        return "FunTranslationsContentsDto{" +
                "translated='" + translated + '\'' +
                '}';
    }
}
