package com.federicogualdi.pokemon.pokedex.rest.dto;

public class FunTranslationsRequestDto {
    public String text;

    public FunTranslationsRequestDto() {
    }

    public FunTranslationsRequestDto(String text) {
        this.text = text;
    }

    @Override
    public String toString() {
        return "FunTranslationsRequestDto{" + "text='" + text + '\'' + '}';
    }
}
