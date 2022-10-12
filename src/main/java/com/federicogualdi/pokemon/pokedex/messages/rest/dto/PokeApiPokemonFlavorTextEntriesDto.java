package com.federicogualdi.pokemon.pokedex.messages.rest.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PokeApiPokemonFlavorTextEntriesDto {
    @JsonProperty("flavor_text")
    public String flavorText;
    public PokeApiPokemonFlavorTextEntriesLanguagesDto language;


    public PokeApiPokemonFlavorTextEntriesDto() {
    }

    public Boolean isEnglish(){
        return "EN".equalsIgnoreCase(language.name);
    }

    @Override
    public String toString() {
        return "PokeApiPokemonFlavorTextEntriesDto{" + "flavorText='" + flavorText + '\'' + ", language=" + language + '}';
    }
}


