package com.federicogualdi.pokemon.pokedex.converter;

import com.federicogualdi.pokemon.pokedex.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.dto.PokeApiPokemonFlavorTextEntriesDto;
import com.federicogualdi.pokemon.pokedex.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.services.TranslatorService;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class PokemonConverter {

    @Inject
    TranslatorService translatorService;

    public PokemonDto from(PokeApiPokemonDto pokemonPokeApi) {
        PokemonDto pokemonConverted = new PokemonDto();
        pokemonConverted.name = pokemonPokeApi.name;
        pokemonConverted.description = pokemonPokeApi.flavorTextEntries.stream()
                .filter(PokeApiPokemonFlavorTextEntriesDto::isEnglish).findFirst()
                .map(d -> d.getFlavorText())
                .orElse(null);
        pokemonConverted.habitat = pokemonPokeApi.habitat.name;
        pokemonConverted.isLegendary = pokemonPokeApi.isLegendary;

        return pokemonConverted;
    }

    public PokemonDto toYodaTranslation(PokemonDto pokemonDto) {
        return translatorService.applyYodaTranslation(pokemonDto);
    }

    public PokemonDto toShakespeareTranslation(PokemonDto pokemonDto) {
        return translatorService.applyShakespeareTranslation(pokemonDto);
    }

}
