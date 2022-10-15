package com.federicogualdi.pokemon.pokedex.rest.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.federicogualdi.pokemon.pokedex.enums.Language;

public class PokeApiPokemonFlavorTextEntriesDto {
    @JsonProperty("flavor_text")
    private String flavorText;
    public PokeApiPokemonFlavorTextEntriesLanguagesDto language;


    public PokeApiPokemonFlavorTextEntriesDto() {
    }

    public String getFlavorText() {
        return flavorText.replaceAll("\\n", " ").replaceAll("\\f", " ");
    }

    public boolean isEnglish() {
        return Language.EN.value().equals(language.name);
    }

    @Override
    public String toString() {
        return "PokeApiPokemonFlavorTextEntriesDto{" + "flavorText='" + flavorText + '\'' + ", language=" + language + '}';
    }
}


